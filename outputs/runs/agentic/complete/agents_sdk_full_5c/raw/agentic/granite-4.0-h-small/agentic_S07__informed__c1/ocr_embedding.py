import os
import boto3
import requests
from google.cloud import embeddings as embeddings_v1

class OCREmbedding:
    def __init__(self, model: str = 'textembedding-gecko'):
        os.environ['WATSONX_API_KEY'] = os.getenv('WATSONX_API_KEY')
        os.environ['WATSONX_PROJECT_ID'] = os.getenv('WATSONX_PROJECT_ID')
        self.model = model
        self.client = embeddings_v1.EmbeddingsClient()

    def embed_text(self, text: str) -> List[float]:
        response = self.client.embed_content(
            project=os.getenv('WATSONX_PROJECT_ID'),
            contents=[{'text': text}],
            model=self.model
        )
        embedding = response.embeddings[0].embedding.data.floats
        return embedding
