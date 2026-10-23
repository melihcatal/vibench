import os
from openai import OpenAI

DEFAULT_OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_embeddings_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def default_embedding_model() -> str:
    return DEFAULT_OPENAI_EMBEDDING_MODEL
