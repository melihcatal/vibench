"""
Local request, response, and normalization helpers for Hosted LLM Inference
and Model-Family Selection.

Supports OpenAI-compatible model families and provides normalization
utilities for chat completion requests and responses.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Iterator


# ---------------------------------------------------------------------------
# Supported model families (OpenAI provider)
# ---------------------------------------------------------------------------

OPENAI_MODEL_FAMILIES = {
    "gpt-4o": "gpt-4o-2024-08-06",
    "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
    "gpt-4-turbo": "gpt-4-turbo-2024-04-09",
    "gpt-3.5-turbo": "gpt-3.5-turbo-0125",
    "text-embedding-3-small": "text-embedding-3-small",
    "text-embedding-3-large": "text-embedding-3-large",
    "tts-1": "tts-1",
    "tts-1-hd": "tts-1-hd",
}

DEFAULT_CHAT_MODEL = OPENAI_MODEL_FAMILIES["gpt-4o"]
DEFAULT_STREAMING_MODEL = OPENAI_MODEL_FAMILIES["gpt-4o-mini"]
DEFAULT_EMBEDDING_MODEL = OPENAI_MODEL_FAMILIES["text-embedding-3-small"]
DEFAULT_TTS_MODEL = OPENAI_MODEL_FAMILIES["tts-1"]


# ---------------------------------------------------------------------------
# Request / Response data structures
# ---------------------------------------------------------------------------

@dataclass
class ChatMessage:
    role: str
    content: str

    def to_openai_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class CompletionRequest:
    messages: List[ChatMessage]
    model: str = DEFAULT_CHAT_MODEL
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    json_mode: bool = False

    def to_openai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [m.to_openai_dict() for m in self.messages],
            "temperature": self.temperature,
            "top_p": self.top_p,
        }
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        if self.json_mode:
            payload["response_format"] = {"type": "json_object"}
        return payload


@dataclass
class StreamRequest:
    messages: List[ChatMessage]
    model: str = DEFAULT_STREAMING_MODEL
    temperature: float = 0.7
    max_tokens: Optional[int] = None

    def to_openai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [m.to_openai_dict() for m in self.messages],
            "temperature": self.temperature,
            "stream": True,
        }
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        return payload


@dataclass
class CompletionResponse:
    content: str
    model: str
    finish_reason: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    @classmethod
    def from_openai(cls, response: Any) -> "CompletionResponse":
        choice = response.choices[0]
        usage = response.usage
        return cls(
            content=choice.message.content or "",
            model=response.model,
            finish_reason=choice.finish_reason,
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
        )


@dataclass
class StreamChunk:
    delta_content: str
    finish_reason: Optional[str] = None

    @classmethod
    def from_openai_chunk(cls, chunk: Any) -> "StreamChunk":
        delta = chunk.choices[0].delta
        return cls(
            delta_content=delta.content or "",
            finish_reason=chunk.choices[0].finish_reason,
        )


@dataclass
class EmbeddingRequest:
    input_text: str
    model: str = DEFAULT_EMBEDDING_MODEL

    def to_openai_payload(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "input": self.input_text,
        }


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    model: str

    @classmethod
    def from_openai(cls, response: Any) -> "EmbeddingResponse":
        return cls(
            embedding=response.data[0].embedding,
            model=response.model,
        )


@dataclass
class ModerationRequest:
    input_text: str

    def to_openai_payload(self) -> Dict[str, str]:
        return {"input": self.input_text}


@dataclass
class ModerationResponse:
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_openai(cls, response: Any) -> "ModerationResponse":
        result = response.results[0]
        return cls(
            flagged=result.flagged,
            categories=dict(result.categories),
            category_scores=dict(result.category_scores),
        )


@dataclass
class TranslationRequest:
    input_text: str
    target_language: str = "en"
    model: str = DEFAULT_CHAT_MODEL

    def to_chat_messages(self) -> List[ChatMessage]:
        system_msg = ChatMessage(
            role="system",
            content=f"Translate the following text into {self.target_language}. "
                    "Provide only the translation with no additional commentary.",
        )
        user_msg = ChatMessage(role="user", content=self.input_text)
        return [system_msg, user_msg]


@dataclass
class SpeechRequest:
    input_text: str
    model: str = DEFAULT_TTS_MODEL
    voice: str = "alloy"
    response_format: str = "mp3"
    speed: float = 1.0

    def to_openai_payload(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "input": self.input_text,
            "voice": self.voice,
            "response_format": self.response_format,
            "speed": self.speed,
        }


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------

def build_chat_request(
    system_prompt: str,
    user_prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    json_mode: bool = False,
) -> CompletionRequest:
    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=user_prompt),
    ]
    return CompletionRequest(
        messages=messages,
        model=model or DEFAULT_CHAT_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
        json_mode=json_mode,
    )


def build_stream_request(
    system_prompt: str,
    user_prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> StreamRequest:
    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=user_prompt),
    ]
    return StreamRequest(
        messages=messages,
        model=model or DEFAULT_STREAMING_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def collect_stream_chunks(chunks: Iterator[StreamChunk]) -> str:
    accumulated: List[str] = []
    for chunk in chunks:
        if chunk.delta_content:
            accumulated.append(chunk.delta_content)
    return "".join(accumulated)


def parse_json_response(content: str) -> Dict[str, Any]:
    cleaned = content.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[len("```json"):].strip()
    if cleaned.startswith("```"):
        cleaned = cleaned[len("```"):].strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()
    return json.loads(cleaned)
