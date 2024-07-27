import gradio as gr  # type: ignore
from transformers import pipeline
from teknofest.main.embeddings import Embeddings

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-tr-en")

embed_model = Embeddings()


def main(message, history):
    # embedding bul -> bu embeddinglerden schemayı dön
    # schemayı ve queryi sqlcoder e ver
    # sql kodunu dön
    en_message = pipe(message)
    en_message = en_message[0]["translation_text"]
    print("User message: ", en_message)
    schema = embed_model.get_relevant_schema(en_message)
    print(schema)
    return str(schema)


demo = gr.ChatInterface(main)

demo.launch()  # share=True
