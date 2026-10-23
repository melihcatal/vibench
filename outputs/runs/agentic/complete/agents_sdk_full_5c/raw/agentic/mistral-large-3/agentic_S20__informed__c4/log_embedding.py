import os
from typing import List
from openai import OpenAI


class LogEmbedder:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_log_messages(self, messages: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=messages
        )
        return [embedding.embedding for embedding in response.data]


if __name__ == "__main__":
    embedder = LogEmbedder()
    embeddings = embedder.embed_log_messages(["Service started", "Database connection failed"])
    print(embeddings)