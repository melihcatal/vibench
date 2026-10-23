import os
from typing import List

import cohere


class TranslationMemoryEmbedder:
    def __init__(self):
        self.client = cohere.Client(os.environ.get('COHERE_API_KEY', ''))

    def embed(self, segments: List[str]) -> List[List[float]]:
        response = self.client.embed(texts=segments, model='embed-english-v3.0', input_type='search_document')
        return response.embeddings
