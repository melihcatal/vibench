import os
from openai import OpenAI


class LogEmbedder:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_log_message(self, message: str) -> List[float]:
        response = self.client.embeddings.create(
            input=message, model="text-embedding-ada-002"
        )
        return response.data[0].embedding


if __name__ == "__main__":
    embedder = LogEmbedder()
    embedding = embedder.embed_log_message("Database connection failed due to timeout.")
    print(embedding[:5])  # Print first 5 dimensions for brevity
