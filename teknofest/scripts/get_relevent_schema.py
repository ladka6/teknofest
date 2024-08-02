import psycopg2  # type: ignore
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()


def get_relevant_schemas(tables_list: List[str]):
    create_table_statements = ""
    try:
        connection_string = os.getenv("DB_URI")
        print(connection_string)
        connection = psycopg2.connect(connection_string)
        cursor = connection.cursor()

        for table in tables_list:
            cursor.execute(
                f"""
                SELECT column_name, data_type, character_maximum_length, numeric_precision, numeric_scale, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = '{table}'
                ORDER BY ordinal_position;
                """
            )
            columns = cursor.fetchall()

            cursor.execute(
                f"""
                SELECT tc.constraint_type, kcu.column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_name = '{table}' AND tc.constraint_type = 'PRIMARY KEY';
                """
            )
            pk_columns = cursor.fetchall()

            pk_columns = [pk[1] for pk in pk_columns]

            create_statement = f"CREATE TABLE {table} (\n"
            for column in columns:
                column_name = column[0]
                data_type = column[1]
                char_length = f"({column[2]})" if column[2] else ""
                num_precision = f"({column[3]},{column[4]})" if column[3] else ""
                not_null = " NOT NULL" if column[5] == "NO" else ""
                default = f" DEFAULT {column[6]}" if column[6] else ""

                create_statement += f"  {column_name} {data_type}{char_length}{num_precision}{not_null}{default},\n"

            if pk_columns:
                pk_columns_str = ", ".join(pk_columns)
                create_statement += f"  PRIMARY KEY ({pk_columns_str}),\n"

            create_statement = create_statement.rstrip(",\n") + "\n);\n\n"
            create_table_statements += create_statement

    except Exception as error:
        print(f"Error fetching schema: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    return create_table_statements
