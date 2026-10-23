import os
import openai
from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.environ.get(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)
OPENAI_EMBEDDING_DIMENSIONS = int(os.environ.get("OPENAI_EMBEDDING_DIMENSIONS", 1536))


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def build_embedding_payload(texts, model=None, dimensions=None):
    model = model or OPENAI_EMBEDDING_MODEL
    payload = {
        "model": model,
        "input": texts if isinstance(texts, list) else [texts],
    }
    if dimensions:
        payload["dimensions"] = dimensions
    return payload


def normalize_embedding_vector(vector):
    magnitude = sum(v * v for v in vector) ** 0.5
    if magnitude == 0:
        return vector
    return [v / magnitude for v in vector]


def extract_embeddings_from_response(response):
    return [item.embedding for item in response.data]


def extract_single_embedding(response):
    return response.data[0].embedding
