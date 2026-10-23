import os
from typing import Any, Iterable, Optional

from openai import AzureOpenAI

from model_models import (
    PlatformRequest,
    PlatformResponse,
    extract_metadata,
    normalize_text,
)


def build_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    )


def choose_model(default: str = "gpt-4o-mini") -> str:
    return os.getenv("AZURE_OPENAI_DEPLOYMENT", default)


def complete(client: AzureOpenAI, request: PlatformRequest) -> PlatformResponse:
    raw = client.responses.create(
        model=request.model or choose_model(),
        input=request.prompt,
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
    )
    return PlatformResponse(
        text=normalize_text(getattr(raw, "output_text", raw)),
        raw=raw,
        metadata=extract_metadata(raw),
    )


def stream_complete(client: AzureOpenAI, request: PlatformRequest) -> Iterable[Any]:
    return client.responses.stream(
        model=request.model or choose_model(),
        input=request.prompt,
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
    )
