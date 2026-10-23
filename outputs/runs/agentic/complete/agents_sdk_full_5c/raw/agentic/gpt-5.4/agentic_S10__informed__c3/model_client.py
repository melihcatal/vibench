from __future__ import annotations

import os
from typing import Iterable, List, Optional

from openai import OpenAI

from model_models import ChatTurn, GenerationConfig, join_text_parts

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


class HostedModelClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv(OPENAI_API_KEY_ENV)
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")
        self.client = OpenAI(api_key=self.api_key, base_url=base_url or OPENAI_BASE_URL)

    def chat_text(self, turns: List[ChatTurn], config: Optional[GenerationConfig] = None) -> str:
        cfg = config or GenerationConfig(model=DEFAULT_OPENAI_MODEL)
        response = self.client.chat.completions.create(
            model=cfg.model,
            temperature=cfg.temperature,
            max_tokens=cfg.max_output_tokens,
            messages=[{"role": t.role, "content": t.content} for t in turns],
        )
        return response.choices[0].message.content or ""

    def stream_chat_text(self, turns: List[ChatTurn], config: Optional[GenerationConfig] = None) -> Iterable[str]:
        cfg = config or GenerationConfig(model=DEFAULT_OPENAI_MODEL)
        stream = self.client.chat.completions.create(
            model=cfg.model,
            temperature=cfg.temperature,
            max_tokens=cfg.max_output_tokens,
            stream=True,
            messages=[{"role": t.role, "content": t.content} for t in turns],
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                yield delta

    def responses_json(self, system_prompt: str, user_prompt: str, model: Optional[str] = None) -> str:
        chosen_model = model or DEFAULT_OPENAI_MODEL
        response = self.client.responses.create(
            model=chosen_model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            text={"format": {"type": "json_object"}},
        )
        if hasattr(response, "output_text"):
            return response.output_text
        output_parts = []
        for item in getattr(response, "output", []):
            for content in getattr(item, "content", []):
                text = getattr(content, "text", None)
                if text:
                    output_parts.append(text)
        return join_text_parts(output_parts)


def build_client() -> HostedModelClient:
    return HostedModelClient()
