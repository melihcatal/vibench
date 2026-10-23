import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

class EmbeddingsClient:
    def __init__(self):
        pass

    def create_embedding(self, text):
        response = openai.Embedding.create(
            input=text,
            model='text-embedding-ada-002'
        )
        return response['data'][0]['embedding']