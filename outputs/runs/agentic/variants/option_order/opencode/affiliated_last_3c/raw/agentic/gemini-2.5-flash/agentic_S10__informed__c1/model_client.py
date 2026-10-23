import os
from openai import OpenAI


class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls._instance.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        return cls._instance

    def get_client(self):
        return self.client
