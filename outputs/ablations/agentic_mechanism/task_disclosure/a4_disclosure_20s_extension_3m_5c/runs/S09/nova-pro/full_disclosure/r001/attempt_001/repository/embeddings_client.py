import os

from embeddingsapi_sdk import EmbeddingsClient


class EmbeddingsAPIClient:
    def __init__(self):
        self.api_key = os.getenv('EMBEDDINGS_API_KEY')
        self.client = EmbeddingsClient(api_key=self.api_key)

    def get_embedding(self, text):
        return self.client.get_embedding(text)

    def batch_embeddings(self, texts):
        return self.client.batch_embeddings(texts)


def configure_client():
    api_key = os.getenv('EMBEDDINGS_API_KEY')
    if not api_key:
        raise ValueError('EMBEDDINGS_API_KEY environment variable not set')
    return EmbeddingsAPIClient()