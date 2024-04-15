import os

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
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    
    def __call__(self, prompt: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_name
        )
        return chat_completion.choices[0].message.content.strip('"')

CHATGPT = ChatGPT()