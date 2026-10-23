import os

API_URL = 'https://api.directembeddings.com/v1'
API_KEY = os.getenv('DIRECT_EMBEDDINGS_API_KEY')

class EmbeddingsClient:
    def __init__(self):
        if not API_KEY:
            raise ValueError('API key must be set in environment variable DIRECT_EMBEDDINGS_API_KEY')
        self.headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }

    def get_embeddings(self, text):
        response = requests.post(
            f'{API_URL}/embeddings',
            headers=self.headers,
            json={'text': text}
        )
        response.raise_for_status()
        return response.json()

# Example usage:
# client = EmbeddingsClient()
# embeddings = client.get_embeddings('Sample text to embed')
# print(embeddings)