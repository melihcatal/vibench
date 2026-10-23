import os
from openai import OpenAI


def get_openai_client(api_key=None, base_url="https://api.openai.com/v1"):
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=key, base_url=base_url)


def build_embedding_payload(model, input_text, dimensions=None):
    payload = {
        "model": model,
        "input": input_text,
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload


def build_batch_embedding_payload(model, input_texts, dimensions=None):
    payload = {
        "model": model,
        "input": input_texts,
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload


def extract_embedding_from_response(response, index=0):
    return response.data[index].embedding


def extract_all_embeddings(response):
    return [item.embedding for item in response.data]


def extract_usage(response):
    return {
        "prompt_tokens": response.usage.prompt_tokens,
        "total_tokens": response.usage.total_tokens,
    }
