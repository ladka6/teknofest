import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline  # type: ignore


class LanguageModel:
    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.tokenizer = self.__get_tokenizer_model("defog/sqlcoder-7b-2")

    def __generate_prompt(
        self, question, metadata_string: str, prompt_file="prompt.md"
    ):
        with open(prompt_file, "r") as f:
            prompt = f.read()

        prompt = prompt.format(
            user_question=question, table_metadata_string=metadata_string
        )
        return prompt

    def __get_tokenizer_model(self, model_name: str):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            use_cache=True,
        ).to(self.device)
        return tokenizer, model

    def run_inference(self, question, metada_string: str, prompt_file="prompt.md"):
        prompt = self.__generate_prompt(question, prompt_file, metada_string)

        eos_token_id = self.tokenizer.eos_token_id
        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device.index if self.device.type == "cuda" else -1,
            max_new_tokens=300,
            do_sample=False,
            return_full_text=False,
            num_beams=5,
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
