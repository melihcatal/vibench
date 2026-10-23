import cohere
import os
import numpy as np


class CohereEmbeddingGenerator:
    def __init__(self):
        self.client = cohere.Client(os.getenv("COHERE_API_KEY"))

    def generate_embedding(self, text: str) -> list:
        response = self.client.embed(
            texts=[text], model="embed-english-v3.0", input_type="search_document"
        )
        return response.embeddings[0]
