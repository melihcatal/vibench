from __future__ import annotations

import os
from typing import Any, Dict, Optional

from openai import AzureOpenAI

from model_models import PlatformRequest, PlatformResponse, normalize_text, normalize_usage


DEFAULT_MODEL = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
DEFAULT_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
DEFAULT_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")


class PlatformClient:
    def __init__(self, endpoint: str = DEFAULT_ENDPOINT, api_key: str = DEFAULT_API_KEY, api_version: str = DEFAULT_API_VERSION):
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_version = api_version
        self._client = AzureOpenAI(
            azure_endpoint=endpoint or None,
            api_key=api_key or None,
            api_version=api_version,
        )

    def select_model(self, preferred_model: Optional[str] = None) -> str:
        return preferred_model or DEFAULT_MODEL

    def invoke(self, request: PlatformRequest) -> PlatformResponse:
        model = self.select_model(request.model_name)
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        raw = self._client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            **request.extra,
        )
        choice = raw.choices[0]
        text = normalize_text(choice.message.content)
        usage = normalize_usage(getattr(raw, "usage", None).model_dump() if hasattr(getattr(raw, "usage", None), "model_dump") else getattr(raw, "usage", None))
        return PlatformResponse(text=text, model_id=model, request_id=getattr(raw, "id", None), usage=usage, raw=raw)

    def stream(self, request: PlatformRequest):
        model = self.select_model(request.model_name)
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        return self._client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True,
            **request.extra,
        )

    def metadata(self, response: PlatformResponse) -> Dict[str, Any]:
        return {
            "model_id": response.model_id,
            "request_id": response.request_id,
            "usage": response.usage,
            "provider": "azure-openai",
        }
