from direct_embeddings_sdk import DirectEmbeddingsClient

class EmbeddingsClient:
    def __init__(self, api_key):
        self.client = DirectEmbeddingsClient(api_key)

    def get_embedding(self, text):
        return self.client.get_embedding(text)

    def batch_embeddings(self, texts):
        return self.client.batch_embeddings(texts)