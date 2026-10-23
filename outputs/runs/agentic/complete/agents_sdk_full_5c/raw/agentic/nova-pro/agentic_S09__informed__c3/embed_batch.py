import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_batch_embeddings(texts):
    response = openai.Embedding.create(
        input=texts,
        model='text-embedding-ada-002'
    )
    return [item['embedding'] for item in response['data']]