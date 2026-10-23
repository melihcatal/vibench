from typing import List, Dict

import os
import requests


class EmbeddingsClient:
    def __init__(self, api_key: str, base_url: str = 'https://api.directembeddings.com'):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def generate_embeddings(self, texts: List[str]) -> Dict[str, List[float]]:
        response = requests.post(
            f'{self.base_url}/embeddings',
            headers=self.headers,
            json={'texts': texts}
        )
        response.raise_for_status()
        return response.json()


def main():
    api_key = os.getenv('DIRECT_EMBEDDINGS_API_KEY')
    if not api_key:
        raise ValueError('DIRECT_EMBEDDINGS_API_KEY environment variable not set')

    client = EmbeddingsClient(api_key=api_key)
    texts = ['Hello, world!', 'This is a test.']
    embeddings = client.generate_embeddings(texts)
    print(embeddings)


if __name__ == '__main__':
    main()