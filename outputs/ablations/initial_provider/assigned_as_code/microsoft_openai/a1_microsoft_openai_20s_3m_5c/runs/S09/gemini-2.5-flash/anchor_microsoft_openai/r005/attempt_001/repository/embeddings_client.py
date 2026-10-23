import os
from openai import OpenAI


class EmbeddingsClient:
    def __init__(self, api_key=None, model='text-embedding-3-small'):
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not provided and not found in environment variables.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def get_embedding(self, text):
        response = self.client.embeddings.create(model=self.model, input=text)
        return response.data[0].embedding

    def get_batch_embeddings(self, texts):
        response = self.client.embeddings.create(model=self.model, input=texts)
        return [item.embedding for item in response.data]