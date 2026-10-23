import os
from openai import OpenAI


def embedding_model():
    return os.environ.get('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')


def get_embeddings_client():
    return OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
