from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

from openai import AzureOpenAI

from model_models import PlatformRequest, PlatformResponse, StreamChunk, normalize_text


@dataclass
class PlatformClientConfig:
    endpoint: str
    api_key: str
    api_version: str = "2024-10-21"
    deployment: str = "gpt-4o-mini"


def load_config() -> PlatformClientConfig:
    return PlatformClientConfig(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
    )


def build_client(config: Optional[PlatformClientConfig] = None) -> AzureOpenAI:
    cfg = config or load_config()
    return AzureOpenAI(azure_endpoint=cfg.endpoint, api_key=cfg.api_key, api_version=cfg.api_version)


def invoke_model(request: PlatformRequest, client: Optional[AzureOpenAI] = None) -> PlatformResponse:
    cfg = load_config()
    sdk = client or build_client(cfg)
    response = sdk.chat.completions.create(
        model=request.model or cfg.deployment,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        **request.extra,
    )
    text = normalize_text(response.choices[0].message.content)
    usage = response.model_dump().get("usage") if hasattr(response, "model_dump") else getattr(response, "usage", None)
    return PlatformResponse(text=text, model=response.model, resource_id=request.model, usage=usage, raw=response)


def stream_model(request: PlatformRequest, client: Optional[AzureOpenAI] = None):
    cfg = load_config()
    sdk = client or build_client(cfg)
    stream = sdk.chat.completions.create(
        model=request.model or cfg.deployment,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
        **request.extra,
    )
    for chunk in stream:
        delta = getattr(chunk.choices[0].delta, "content", None)
        if delta:
            yield StreamChunk(text=delta, raw=chunk)


def select_resource(model_name: str) -> str:
    cfg = load_config()
    if model_name.startswith("azure/"):
        return model_name.split("/", 1)[1]
    return model_name or cfg.deployment
