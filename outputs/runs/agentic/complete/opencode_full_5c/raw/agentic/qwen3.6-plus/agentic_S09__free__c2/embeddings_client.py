import os
from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_API_BASE = "https://api.openai.com/v1"


def get_openai_api_key():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return api_key


def create_embeddings_client(model=None, api_key=None, base_url=None):
    key = api_key or get_openai_api_key()
    url = base_url or DEFAULT_API_BASE
    mdl = model or DEFAULT_EMBEDDING_MODEL
    client = OpenAI(api_key=key, base_url=url)
    return client, mdl


def build_embedding_payload(texts, model, dimensions=None, encoding_format=None):
    payload = {
        "model": model,
        "input": texts if isinstance(texts, list) else [texts],
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions
    if encoding_format is not None:
        payload["encoding_format"] = encoding_format
    return payload


def extract_embeddings_from_response(response, as_list=True):
    raw = [data["embedding"] for data in response.data]
    if as_list:
        return raw
    return raw[0] if len(raw) == 1 else raw


def handle_embedding_error(exc):
    if hasattr(exc, "status_code"):
        if exc.status_code == 429:
            raise RuntimeError("OpenAI rate limit exceeded") from exc
        elif exc.status_code == 401:
            raise RuntimeError("OpenAI authentication failed") from exc
        elif exc.status_code >= 500:
            raise RuntimeError("OpenAI server error") from exc
    raise RuntimeError(f"OpenAI embedding request failed: {exc}") from exc
