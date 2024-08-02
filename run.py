import gradio as gr  # type: ignore
from transformers import pipeline  # type: ignore
from teknofest.main.embeddings import Embeddings
from teknofest.scripts import get_relevent_schema
from teknofest.main.language_model import LanguageModel

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-tr-en")

embed_model = Embeddings()
model = LanguageModel()


def main(message, history):
    en_message = pipe(message)
    en_message = en_message[0]["translation_text"]
    schema = embed_model.get_relevant_schema(message)
    # [{'type': 'table', 'name': 'employees'}]
    db_schema = []
    for table in schema:
        db_schema.append(table["name"])
    db_metadata = get_relevent_schema.get_relevant_schemas(db_schema)

    return "ege"
    # return str(schema)


demo = gr.ChatInterface(main)

demo.launch()  # share=True
