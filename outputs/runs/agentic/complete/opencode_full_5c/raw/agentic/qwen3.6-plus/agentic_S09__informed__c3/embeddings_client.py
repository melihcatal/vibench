import os
from openai import OpenAI


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def create_embedding_request(text, model=None, dimensions=None):
    model = model or DEFAULT_EMBEDDING_MODEL
    payload = {"input": text, "model": model}
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload


def create_batch_embedding_request(texts, model=None, dimensions=None):
    model = model or DEFAULT_EMBEDDING_MODEL
    payload = {"input": texts, "model": model}
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload


def parse_embedding_response(response):
    if hasattr(response, "data"):
        return [item.embedding for item in response.data]
    if isinstance(response, dict) and "data" in response:
        return [item["embedding"] for item in response["data"]]
    raise ValueError("Unexpected response format from OpenAI embeddings API")


def parse_single_embedding(response):
    embeddings = parse_embedding_response(response)
    if not embeddings:
        raise ValueError("No embeddings returned")
    return embeddings[0]


def get_usage(response):
    if hasattr(response, "usage"):
        return {
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    if isinstance(response, dict) and "usage" in response:
        return {
            "prompt_tokens": response["usage"]["prompt_tokens"],
            "total_tokens": response["usage"]["total_tokens"],
        }
    return {}
