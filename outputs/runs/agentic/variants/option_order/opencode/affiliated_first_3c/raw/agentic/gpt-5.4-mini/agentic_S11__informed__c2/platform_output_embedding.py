import os
from openai import OpenAI

def platform_output_embedding(text: str):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    return client.embeddings.create(model=os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small'), input=text)
