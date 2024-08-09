import os
import pandas as pd  # type: ignore
from sqlalchemy import create_engine
import unicodedata


def turkish_to_english(text):
    # Normalize the text to decompose characters with diacritics
    text = unicodedata.normalize("NFKD", text)
    turkish_chars = {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
        "Ç": "C",
        "Ğ": "G",
        "İ": "I",
        "Ö": "O",
        "Ş": "S",
        "Ü": "U",
    }
    for turkish_char, english_char in turkish_chars.items():
        text = text.replace(turkish_char, english_char)
    # Remove diacritic marks
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text


def csv_to_postgresql(directory_path, db_uri):
    # Create a SQLAlchemy engine
    engine = create_engine(db_uri)

    # List all CSV files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory_path, file_name)

            # Try reading the CSV file with different encodings
            encodings = ["utf-8", "latin1", "ISO-8859-1"]
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    print(f"Successfully read {file_name} with encoding {encoding}")
                    break
                except UnicodeDecodeError:
                    print(
                        f"Could not decode file {file_name} with encoding {encoding}. Trying next encoding..."
                    )
            else:
                print(
                    f"Failed to read {file_name} with available encodings. Skipping this file."
                )
                continue

            # Convert all column names to lowercase and replace Turkish characters
            df.columns = [turkish_to_english(col.lower()) for col in df.columns]

            # Convert all string values in the DataFrame to lowercase and replace Turkish characters
            df = df.applymap(
                lambda x: turkish_to_english(x.lower()) if isinstance(x, str) else x
            )

            # Use the file name (without extension) as the table name
            table_name = turkish_to_english(os.path.splitext(file_name)[0].lower())

            # Write the data to a PostgreSQL table
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            print(
                f"Data from '{file_name}' has been successfully written to table '{table_name}' in the PostgreSQL database."
            )
