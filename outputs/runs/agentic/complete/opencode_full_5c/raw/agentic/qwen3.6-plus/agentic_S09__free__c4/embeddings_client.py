import os
from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_EMBEDDING_DIMENSIONS = 1536


def get_openai_client(api_key=None, base_url=None):
    key = api_key or OPENAI_API_KEY
    url = base_url or OPENAI_API_BASE
    return OpenAI(api_key=key, base_url=url)


def create_embedding_payload(texts, model=None, dimensions=None):
    model_id = model or DEFAULT_EMBEDDING_MODEL
    payload = {"input": texts, "model": model_id}
    if dimensions:
        payload["dimensions"] = dimensions
    return payload


def extract_embeddings(response):
    if hasattr(response, "data"):
        return [item.embedding for item in response.data]
    if isinstance(response, dict) and "data" in response:
        return [item["embedding"] for item in response["data"]]
    raise ValueError("Unexpected response format")


def handle_openai_error(exc):
    if hasattr(exc, "status_code"):
        if exc.status_code == 429:
            raise RuntimeError("Rate limit exceeded by OpenAI API") from exc
        elif exc.status_code == 401:
            raise RuntimeError("Invalid OpenAI API key") from exc
        elif exc.status_code >= 500:
            raise RuntimeError("OpenAI API server error") from exc
    raise RuntimeError(f"OpenAI API error: {exc}") from exc
