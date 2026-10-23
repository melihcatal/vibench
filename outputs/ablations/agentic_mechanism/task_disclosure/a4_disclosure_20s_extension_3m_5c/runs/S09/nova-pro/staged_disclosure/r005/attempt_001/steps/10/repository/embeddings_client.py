import os

from direct_embeddings_sdk import DirectEmbeddingsClient


class EmbeddingsClient:
    def __init__(self):
        self.api_key = os.getenv('DIRECT_EMBEDDINGS_API_KEY')
        self.client = DirectEmbeddingsClient(api_key=self.api_key)

    def create_embedding(self, text):
        return self.client.create_embedding(text=text)


if __name__ == '__main__':
    client = EmbeddingsClient()
    sample_text = 'This is a sample text for embedding.'
    embedding = client.create_embedding(sample_text)
    print(embedding)