import cohere
from typing import List


class CohereEmbeddingGenerator:
    def __init__(self):
        self.client = cohere.Client(api_key=open(".cohere_api_key").read().strip())

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embed(
            texts=texts,
            model="embed-multilingual-v3.0",
        )
        return response.embeddings


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    generator = CohereEmbeddingGenerator()
    return generator.generate_embeddings(segments)