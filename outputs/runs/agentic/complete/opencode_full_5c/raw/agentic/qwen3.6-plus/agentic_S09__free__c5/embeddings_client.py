import os
from typing import Optional
from openai import OpenAI
from embeddings_models import (
    EmbeddingRequest,
    BatchEmbeddingRequest,
    EmbeddingResponse,
    BatchEmbeddingResponse,
    build_openai_payload,
    build_openai_batch_payload,
    parse_openai_response,
    parse_openai_batch_response,
)

OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_EMBEDDINGS_ENDPOINT = "/embeddings"


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for OpenAI embeddings API"
        )
    return api_key


def create_openai_client(
    api_key: Optional[str] = None, base_url: str = OPENAI_API_BASE
) -> OpenAI:
    key = api_key or get_openai_api_key()
    return OpenAI(api_key=key, base_url=base_url)


def build_embeddings_client(api_key: Optional[str] = None) -> OpenAI:
    return create_openai_client(api_key=api_key)


def normalize_request(request: EmbeddingRequest) -> EmbeddingRequest:
    if not request.model:
        request.model = "text-embedding-3-small"
    if not request.encoding_format:
        request.encoding_format = "float"
    return request


def normalize_batch_request(request: BatchEmbeddingRequest) -> BatchEmbeddingRequest:
    if not request.model:
        request.model = "text-embedding-3-small"
    if not request.encoding_format:
        request.encoding_format = "float"
    return request


def call_embeddings_api(
    client: OpenAI,
    request: EmbeddingRequest,
) -> EmbeddingResponse:
    request = normalize_request(request)
    payload = build_openai_payload(request)
    response = client.embeddings.create(
        model=payload["model"],
        input=payload["input"],
        encoding_format=payload["encoding_format"],
        dimensions=payload.get("dimensions"),
    )
    response_data = {
        "data": [{"embedding": response.data[0].embedding, "index": 0}],
        "model": response.model,
        "usage": {"prompt_tokens": response.usage.prompt_tokens},
    }
    return parse_openai_response(response_data, input_text=request.input_text)


def call_batch_embeddings_api(
    client: OpenAI,
    request: BatchEmbeddingRequest,
) -> BatchEmbeddingResponse:
    request = normalize_batch_request(request)
    payload = build_openai_batch_payload(request)
    response = client.embeddings.create(
        model=payload["model"],
        input=payload["input"],
        encoding_format=payload["encoding_format"],
        dimensions=payload.get("dimensions"),
    )
    response_data = {
        "data": [
            {"embedding": item.embedding, "index": item.index} for item in response.data
        ],
        "model": response.model,
        "usage": {"prompt_tokens": response.usage.prompt_tokens},
    }
    return parse_openai_batch_response(response_data, input_texts=request.input_texts)


def load_config_from_env() -> dict:
    return {
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
        "base_url": os.environ.get("OPENAI_API_BASE", OPENAI_API_BASE),
        "default_model": os.environ.get(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        ),
        "default_dimensions": int(os.environ.get("OPENAI_EMBEDDING_DIMENSIONS", "0"))
        or None,
    }
