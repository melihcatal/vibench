from typing import List, Dict
import cohere
import os


class LogEmbedder:
    def __init__(self):
        self.client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

    def embed_logs(self, log_messages: List[str]) -> List[Dict[str, List[float]]]:
        response = self.client.embed(texts=log_messages, model="embed-english-v3.0")
        return [{"message": msg, "embedding": emb} for msg, emb in zip(log_messages, response.embeddings)]


if __name__ == "__main__":
    embedder = LogEmbedder()
    sample_logs = ["Database connection failed", "User login successful"]
    print(embedder.embed_logs(sample_logs))