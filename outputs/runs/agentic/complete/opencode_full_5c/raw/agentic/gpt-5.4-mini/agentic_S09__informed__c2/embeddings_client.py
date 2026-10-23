import os
from openai import OpenAI


def get_openai_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise EnvironmentError("OPENAI_API_KEY is required for OpenAI embeddings")
    return key


def get_embeddings_client():
    return OpenAI(api_key=get_openai_api_key())
