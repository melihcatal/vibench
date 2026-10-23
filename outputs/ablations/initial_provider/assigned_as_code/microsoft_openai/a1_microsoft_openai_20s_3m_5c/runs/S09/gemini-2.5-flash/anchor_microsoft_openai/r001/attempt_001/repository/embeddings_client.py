import os
from openai import OpenAI

class EmbeddingsClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found. Please set the environment variable or pass it directly.")
        self.client = OpenAI(api_key=self.api_key)

    def get_client(self):
        return self.client
