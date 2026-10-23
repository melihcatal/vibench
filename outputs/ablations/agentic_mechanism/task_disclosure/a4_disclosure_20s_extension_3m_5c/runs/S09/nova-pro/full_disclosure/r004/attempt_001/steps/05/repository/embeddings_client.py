import os
from openai import AzureOpenAI

class EmbeddingsClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            api_version='2023-05-15',
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
        )

    def get_embedding(self, text):
        response = self.client.embeddings.create(
            input=text,
            model='text-embedding-ada-002'
        )
        return response.data[0].embedding