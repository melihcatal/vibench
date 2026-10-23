import os
from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


def get_openai_client(
    api_key: str | None = None, base_url: str | None = None
) -> OpenAI:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    url = base_url or OPENAI_API_BASE
    return OpenAI(api_key=key, base_url=url)


def normalize_payload(text: str) -> str:
    return text.strip()


def normalize_payload_batch(texts: list[str]) -> list[str]:
    return [normalize_payload(t) for t in texts if t.strip()]


def parse_embedding_response(response) -> list[float]:
    return response.data[0].embedding


def parse_batch_embedding_response(response) -> list[list[float]]:
    sorted_data = sorted(response.data, key=lambda d: d.index)
    return [item.embedding for item in sorted_data]


def get_model_info(model: str) -> dict:
    model_configs = {
        "text-embedding-3-small": {"dimensions": 1536, "max_input_tokens": 8191},
        "text-embedding-3-large": {"dimensions": 3072, "max_input_tokens": 8191},
        "text-embedding-ada-002": {"dimensions": 1536, "max_input_tokens": 8191},
    }
    return model_configs.get(model, {"dimensions": 1536, "max_input_tokens": 8191})
