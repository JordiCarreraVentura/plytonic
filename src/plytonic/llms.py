import os
from typing import Dict, List, Union

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ChatGPT:

    def __init__(
        self,
        *args,
        **kwargs
    ):
        """


        Parameters
        ----------

        model_name: str
            gpt-3.5

        max_tokens: int
            1024


        """
        params = {
            "model_name": "gpt-4",
            "max_tokens": 1024
        }

        # Set up your OpenAI API key
        params.update(dict(kwargs))
        self.__dict__.update(params)
        self.client = None

    def __set_client(self) -> None:
        if self.client:
            return
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    def __call__(self, prompt: str, history: List[Dict[str, str]] = []) -> str:
        self.__set_client()
        chat_completion = self.client.chat.completions.create(
            messages=history + [{"role": "user", "content": prompt}],
            max_tokens=4096,
            model=self.model_name
        )
        return chat_completion.choices[0].message.content.strip('"')




CHATGPT = ChatGPT()


if __name__ == '__main__':

    print(CHATGPT("""please, provide code that, given a list of documents as strings, "
    "uses DistilBERTa to encode them, then applies a suitable dimensionality "
    "reduction method to make the embeddings more easily handled by a clustering "
    "algorithm, and finally use HDBSCAN on the document embeddings to get a final "
    "set of topics."""))
    exit()

    messages = []
    for _ in range(5):
        prompt = "tell me a joke, please! Please be creative!"
        response = CHATGPT(prompt, history=messages)
        messages.append({"role": "user", "content": prompt})
        messages.append({"role": "system", "content": response})
        print(messages)
        print(response)