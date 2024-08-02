from sqlalchemy import create_engine, inspect


def get_database_schema(connection_string):
    # Create the engine
    engine = create_engine(connection_string)

    # Create the inspector
    inspector = inspect(engine)

    # Get all table names
    tables = inspector.get_table_names()

    # Create the schema dictionary
    schema_dict = {}

    # Iterate through tables and get their columns
    for table in tables:
        columns = inspector.get_columns(table)
        column_names = [column["name"] for column in columns]
        schema_dict[table] = column_names

    return schema_dict


# Connection string for the PostgreSQL database
connection_string = "postgresql://postgres:postgres@127.0.0.1:5432/postgres"

# Get the schema dictionary
schema = get_database_schema(connection_string)

# Print the schema dictionary
print(schema)
