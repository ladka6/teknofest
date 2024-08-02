import pandas as pd
from sqlalchemy import create_engine


def xlsx_to_postgresql(file_path, db_uri):
    # Read the Excel file with all sheets
    excel_data = pd.read_excel(file_path, sheet_name=None)

    # Create a SQLAlchemy engine
    engine = create_engine(db_uri)

    for sheet_name, df in excel_data.items():

        # Write the data to a PostgreSQL table
        df.to_sql(sheet_name, engine, if_exists="replace", index=False)
        print(
            f"Data from sheet '{sheet_name}' has been successfully written to table '{sheet_name}' in the PostgreSQL database."
        )


if __name__ == "__main__":
    # File path of the Excel file
    file_path = "/Users/ladka6/Projects/teknofest-be/teknofest/data/2023-kutuphane-ve-muzeler-mudurlugu-okuyucu-istatistikleri.xlsx"

    # PostgreSQL database URI
    db_uri = "postgresql://postgres:postgres@127.0.0.1:5432/postgres"

    xlsx_to_postgresql(file_path, db_uri)
