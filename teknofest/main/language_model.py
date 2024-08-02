import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline  # type: ignore


class LanguageModel:
    def __init__(self) -> None:
        self.model, self.tokenizer = self.__get_tokenizer_model("defog/sqlcoder-7b-2")

    def generate_prompt(
        self, question, prompt_file="prompt.md", metadata_file="metadata.sql"
    ):
        with open(prompt_file, "r") as f:
            prompt = f.read()

        with open(metadata_file, "r") as f:
            table_metadata_string = f.read()

        prompt = prompt.format(
            user_question=question, table_metadata_string=table_metadata_string
        )
        return prompt

    def __get_tokenizer_model(self, model_name):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto",
            use_cache=True,
        )
        return tokenizer, model

    def run_inference(
        self, question, prompt_file="prompt.md", metadata_file="metadata.sql"
    ):
        prompt = self.generate_prompt(question, prompt_file, metadata_file)

        # make sure the model stops generating at triple ticks
        # eos_token_id = tokenizer.convert_tokens_to_ids(["```"])[0]
        eos_token_id = self.tokenizer.eos_token_id
        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=300,
            do_sample=False,
            return_full_text=False,  # added return_full_text parameter to prevent splitting issues with prompt
            num_beams=5,  # do beam search with 5 beams for high quality results
        )
        generated_query = (
            pipe(
                prompt,
                num_return_sequences=1,
                eos_token_id=eos_token_id,
                pad_token_id=eos_token_id,
            )[0]["generated_text"]
            .split(";")[0]
            .split("```")[0]
            .strip()
            + ";"
        )
        return generated_query
