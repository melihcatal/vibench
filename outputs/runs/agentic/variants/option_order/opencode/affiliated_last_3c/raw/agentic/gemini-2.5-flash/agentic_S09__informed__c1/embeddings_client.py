import os
from openai import OpenAI


class EmbeddingsClient:
    def __init__(self):
        self._client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self._embedding_model = "text-embedding-ada-002"  # OpenAI model

    def get_client(self) -> OpenAI:
        return self._client

    def get_embedding_model(self) -> str:
        return self._embedding_model
