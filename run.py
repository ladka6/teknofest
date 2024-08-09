import gradio as gr  # type: ignore
from teknofest.scripts.csv_to_sql import csv_to_postgresql
from teknofest.main.embeddings import Embeddings
from teknofest.scripts import sql_functions
from teknofest.main.language_model import LanguageModel
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

load_dotenv()

csv_to_postgresql("teknofest/data", os.getenv("DB_URI"))

embed_model = Embeddings()
model = LanguageModel()


def run_query(query: str) -> list:
    db_uri = os.getenv("DB_URI") or ""
    engine = create_engine(db_uri)
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            columns = result.keys()
            rows = result.fetchall()

            data_list = [dict(zip(columns, row)) for row in rows]
            return data_list
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        return []


def main(message, history):
    schema = embed_model.get_relevant_schema(message)
    db_schema = []
    for table in schema:
        db_schema.append(table["name"])
    db_metadata = sql_functions.get_relevant_schemas(db_schema)
    sql_query = model.run_inference(message, db_metadata)
    print("Out of the sql query: ", sql_query)
    sql_data = run_query(sql_query)

    if sql_data:
        df = pd.DataFrame(sql_data)
        sql_data_html = df.to_html(index=False)
    else:
        sql_data_html = "<p>No results found.</p>"

    print(sql_data)
    print()
    return f"<pre>{sql_query}</pre><br>{sql_data_html}"


demo = gr.ChatInterface(
    main,
    chatbot=gr.Chatbot(
        value=[
            (
                None,
                f"Merhaba 👋. Ben bir database asistanıyım. Bana sorabileceğiniz örnek sorular\n {model.get_list_of_questions()}",
            )
        ]
    ),
)

demo.launch()
