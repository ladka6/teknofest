import gradio as gr  # type: ignore
from teknofest.scripts.csv_to_sql import csv_to_postgresql
from transformers import pipeline  # type: ignore
from teknofest.main.embeddings import Embeddings
from teknofest.scripts import get_relevent_schema
from teknofest.main.language_model import LanguageModel
import os
from dotenv import load_dotenv

load_dotenv()

csv_to_postgresql("teknofest/data", os.getenv("DB_URI"))

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-tr-en")

embed_model = Embeddings()
model = LanguageModel()


def main(message, history):
    en_message = pipe(message)
    en_message = en_message[0]["translation_text"]
    schema = embed_model.get_relevant_schema(message)
    db_schema = []
    for table in schema:
        db_schema.append(table["name"])
    db_metadata = get_relevent_schema.get_relevant_schemas(db_schema)
    sql_query = model.run_inference(en_message, db_metadata)
    return sql_query


demo = gr.ChatInterface(main)

demo.launch(share=True)
