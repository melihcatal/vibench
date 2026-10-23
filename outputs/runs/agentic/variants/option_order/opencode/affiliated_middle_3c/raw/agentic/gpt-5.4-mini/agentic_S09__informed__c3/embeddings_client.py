import os
from openai import OpenAI


def default_embedding_model():
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_embeddings_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
