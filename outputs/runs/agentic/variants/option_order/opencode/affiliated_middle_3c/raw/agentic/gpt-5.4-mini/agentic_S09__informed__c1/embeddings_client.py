import os
from dataclasses import dataclass
from openai import OpenAI

DEFAULT_OPENAI_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')


def default_embedding_model() -> str:
    return DEFAULT_OPENAI_EMBEDDING_MODEL


def get_embeddings_client() -> OpenAI:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY is required')
    return OpenAI(api_key=api_key)
