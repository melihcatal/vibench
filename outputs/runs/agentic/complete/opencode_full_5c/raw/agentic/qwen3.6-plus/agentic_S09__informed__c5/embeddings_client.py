import os
from openai import OpenAI


DEFAULT_MODEL = "text-embedding-3-small"
DEFAULT_DIMENSIONS = 1536


def get_openai_client(api_key=None):
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def build_embedding_payload(text, model=DEFAULT_MODEL, dimensions=None):
    payload = {"input": text, "model": model}
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload


def normalize_embedding_response(response, dimensions=None):
    if isinstance(response, list):
        data = response
    elif hasattr(response, "data"):
        data = response.data
    else:
        data = response.get("data", [])

    embeddings = []
    for item in data:
        if hasattr(item, "embedding"):
            vec = item.embedding
        else:
            vec = item.get("embedding", [])
        if dimensions is not None:
            vec = vec[:dimensions]
        embeddings.append(vec)
    return embeddings


def extract_usage(response):
    if hasattr(response, "usage"):
        return {
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    if isinstance(response, dict) and "usage" in response:
        return response["usage"]
    return {}
