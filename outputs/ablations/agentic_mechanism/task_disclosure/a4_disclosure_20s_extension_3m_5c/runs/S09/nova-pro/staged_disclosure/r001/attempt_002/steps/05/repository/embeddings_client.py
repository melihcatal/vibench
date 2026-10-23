from direct_embeddings_sdk import DirectEmbeddingsClient

class EmbeddingsClient:
    def __init__(self, api_key):
        self.client = DirectEmbeddingsClient(api_key)

    def get_embeddings(self, text):
        return self.client.get_embeddings(text)

# Example usage:
# client = EmbeddingsClient('your_api_key')
# embeddings = client.get_embeddings('sample text')