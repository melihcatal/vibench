from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class LLMRequest:
    model: str = "gpt-4o"
    prompt: str = ""
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0
    stop: Optional[list[str]] = None
    json_mode: bool = False
    stream: bool = False

    def to_openai_payload(self) -> dict[str, Any]:
        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.prompt})
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "stream": self.stream,
        }
        if self.stop:
            payload["stop"] = self.stop
        if self.json_mode:
            payload["response_format"] = {"type": "json_object"}
        return payload


@dataclass
class LLMResponse:
    text: str = ""
    model_used: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    finish_reason: str = ""
    raw: Optional[dict[str, Any]] = None

    @classmethod
    def from_openai(cls, response_obj: Any) -> LLMResponse:
        choice = response_obj.choices[0]
        usage = response_obj.usage
        return cls(
            text=choice.message.content or "",
            model_used=response_obj.model,
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
            finish_reason=choice.finish_reason or "",
            raw=response_obj.model_dump()
            if hasattr(response_obj, "model_dump")
            else None,
        )


@dataclass
class StreamChunk:
    delta: str = ""
    index: int = 0
    finish_reason: Optional[str] = None
    model_used: str = ""


@dataclass
class EmbeddingResponse:
    embedding: list[float] = field(default_factory=list)
    model_used: str = ""
    usage_tokens: int = 0
    raw: Optional[dict[str, Any]] = None

    @classmethod
    def from_openai(cls, response_obj: Any) -> EmbeddingResponse:
        data = response_obj.data[0]
        return cls(
            embedding=data.embedding,
            model_used=response_obj.model,
            usage_tokens=response_obj.usage.total_tokens if response_obj.usage else 0,
            raw=response_obj.model_dump()
            if hasattr(response_obj, "model_dump")
            else None,
        )


@dataclass
class SafetyResponse:
    is_safe: bool = True
    categories: dict[str, bool] = field(default_factory=dict)
    category_scores: dict[str, float] = field(default_factory=dict)
    flagged_categories: list[str] = field(default_factory=list)
    raw: Optional[dict[str, Any]] = None


@dataclass
class TranslationResponse:
    translated_text: str = ""
    source_language: str = ""
    target_language: str = "en"
    model_used: str = ""
    raw: Optional[dict[str, Any]] = None


@dataclass
class SpokenBriefResponse:
    text: str = ""
    audio_url: Optional[str] = None
    model_used: str = ""
    voice: str = "alloy"
    raw: Optional[dict[str, Any]] = None


def normalize_prompt(prompt: str, max_length: int = 128000) -> str:
    return prompt[:max_length].strip()


def normalize_system_prompt(system: str) -> str:
    return system.strip()


def extract_json_from_text(text: str) -> Optional[dict[str, Any]]:
    text = text.strip()
    if text.startswith("```json"):
        text = text[len("```json") :].strip()
    if text.startswith("```"):
        text = text[len("```") :].strip()
    if text.endswith("```"):
        text = text[:-3].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
