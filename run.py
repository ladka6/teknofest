import gradio as gr  # type: ignore
from transformers import pipeline  # type: ignore
from teknofest.main.embeddings import Embeddings

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-tr-en")

embed_model = Embeddings()


def main(message, history):
    en_message = pipe(message)
    en_message = en_message[0]["translation_text"]
    schema = embed_model.get_relevant_schema(message)
    # [{'type': 'table', 'name': 'employees'}]
    return str(schema)


demo = gr.ChatInterface(main)

demo.launch()  # share=True
