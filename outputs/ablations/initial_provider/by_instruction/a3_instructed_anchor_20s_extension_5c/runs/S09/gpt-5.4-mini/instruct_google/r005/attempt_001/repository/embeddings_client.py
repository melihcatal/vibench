import os
from functools import lru_cache

from google import genai


def _env(name, default=None):
    value = os.getenv(name)
    return value if value else default


def default_model():
    return _env("GOOGLE_EMBEDDING_MODEL", "text-embedding-004")


def api_key():
    return _env("GOOGLE_API_KEY")


@lru_cache(maxsize=1)
def client():
    return genai.Client(api_key=api_key())


def embed_contents(contents, model=None):
    return client().models.embed_content(model=model or default_model(), contents=contents)


def embed_query(text, model=None):
    return embed_contents(text, model=model)


def embed_texts(texts, model=None):
    return embed_contents(texts, model=model)
