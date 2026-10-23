import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def get_client(self) -> OpenAI:
        return self.client
