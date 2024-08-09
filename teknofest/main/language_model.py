import torch
from openai import OpenAI
from teknofest.scripts.sql_functions import get_table_metada
import os
from dotenv import load_dotenv

load_dotenv()


class LanguageModel:
    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.tokenizer, self.model = self.__get_tokenizer_model("defog/sqlcoder-7b-2")
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    def __generate_prompt(
        self,
        question,
        metadata_string: str,
        prompt_file="/Users/ladka6/Projects/teknofest-be/promt.md",
    ):
        with open(prompt_file, "r") as f:
            prompt = f.read()

        prompt = prompt.format(
            user_question=question, table_metadata_string=metadata_string
        )
        return prompt

    # def __get_tokenizer_model(self, model_name: str):
    #     tokenizer = AutoTokenizer.from_pretrained(model_name)
    #     model = AutoModelForCausalLM.from_pretrained(
    #         model_name,
    #         trust_remote_code=True,
    #         torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    #         device_map="auto" if torch.cuda.is_available() else None,
    #         use_cache=True,
    #     ).to(self.device)
    #     return tokenizer, model

    def run_inference(
        self,
        question,
        metada_string: str,
    ):
        prompt = self.__generate_prompt(
            question=question, metadata_string=metada_string
        )

        # eos_token_id = self.tokenizer.eos_token_id
        # pipe = pipeline(
        #     "text-generation",
        #     model=self.model,
        #     tokenizer=self.tokenizer,
        #     device=self.device.index if self.device.type == "cuda" else -1,
        #     max_new_tokens=300,
        #     do_sample=False,
        #     return_full_text=False,
        #     num_beams=5,
        # )
        # generated_query = (
        #     pipe(
        #         prompt,
        #         num_return_sequences=1,
        #         eos_token_id=eos_token_id,
        #         pad_token_id=eos_token_id,
        #     )[0]["generated_text"]
        #     .split(";")[0]
        #     .split("```")[0]
        #     .strip()
        #     + ";"
        # return generated_query
        print(prompt)
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Sen bir database menajerisin. Sana sorulan sorular SQL Sorgusu yazarak yanıtlayacaksın\n "
                    "Sadece SQL sorgusunu yaz, herhangi bir özel karakter veya cümle ekleme cevabı özel bir şekilde dönme düz string olarak dön"
                    "SQL Queryleri yazarken tablo isimlerini türkçeye çevirme"
                    "Örnek soru: Tüm WiFi abonelerinin sayısını toplamda hesapla."
                    "Örnek Cevap: SELECT SUM(number_of_subscriber) FROM ibb_wifi_subscriber;"
                    "Örnek soru: Tüm tiyatro oyunlarının isimlerini ve tarihlerini listele."
                    "Örnek Cevap: SELECT oyun_adi, tarih FROM theater_play;",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content

    def get_list_of_questions(self):
        table_metadata = get_table_metada()
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Sen bir database menajerisin.\n Sadece istenilen soruları yaz, herhangi bir özel karakter veya cümle ekleme.",
                },
                {
                    "role": "user",
                    "content": f"Verilen SQL Metadası icin: \n {table_metadata} \n 10 farklı SQL yazabileceğim sorgu sorusu yaz",
                },
            ],
        )
        return completion.choices[0].message.content
