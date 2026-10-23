from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModelRequest:
    model_id: str
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.8
    stream: bool = False
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def to_messages(self) -> List[Dict[str, str]]:
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass
class ModelResponse:
    content: str
    model_id: str
    request_id: str = ""
    finish_reason: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    raw_response: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StreamChunk:
    content: str
    index: int = 0
    finish_reason: Optional[str] = None
    raw_chunk: Optional[Any] = None


@dataclass
class StreamedResponse:
    content: str
    model_id: str
    request_id: str = ""
    finish_reason: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    chunks: List[StreamChunk] = field(default_factory=list)
    raw_response: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyResult:
    is_safe: bool
    categories: Dict[str, float]
    flagged_categories: List[str]
    raw_response: Optional[Any] = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    raw_response: Optional[Any] = None


@dataclass
class EmbeddingResult:
    embeddings: List[List[float]]
    model_id: str
    input_tokens: int = 0
    raw_response: Optional[Any] = None


@dataclass
class AudioResult:
    audio_url: Optional[str] = None
    audio_data: Optional[bytes] = None
    model_id: str = ""
    request_id: str = ""
    raw_response: Optional[Any] = None


def normalize_dashscope_completion(response: Any) -> ModelResponse:
    output = response.output
    usage = response.usage
    return ModelResponse(
        content=output.text if hasattr(output, "text") else output.get("text", ""),
        model_id=response.model
        if hasattr(response, "model")
        else response.get("model", ""),
        request_id=response.request_id
        if hasattr(response, "request_id")
        else response.get("request_id", ""),
        finish_reason=getattr(output, "finish_reason", "")
        or output.get("finish_reason", ""),
        input_tokens=getattr(usage, "input_tokens", 0) or usage.get("input_tokens", 0),
        output_tokens=getattr(usage, "output_tokens", 0)
        or usage.get("output_tokens", 0),
        total_tokens=getattr(usage, "total_tokens", 0) or usage.get("total_tokens", 0),
        raw_response=response,
        metadata={
            "model": response.model
            if hasattr(response, "model")
            else response.get("model", ""),
            "request_id": response.request_id
            if hasattr(response, "request_id")
            else response.get("request_id", ""),
        },
    )


def normalize_dashscope_stream(response: Any) -> StreamedResponse:
    full_content = []
    chunks = []
    request_id = ""
    model_id = ""
    finish_reason = ""
    input_tokens = 0
    output_tokens = 0
    total_tokens = 0

    for chunk in response:
        request_id = (
            chunk.request_id
            if hasattr(chunk, "request_id")
            else chunk.get("request_id", "")
        )
        model_id = chunk.model if hasattr(chunk, "model") else chunk.get("model", "")
        output_data = (
            chunk.output if hasattr(chunk, "output") else chunk.get("output", {})
        )
        text = (
            output_data.text
            if hasattr(output_data, "text")
            else output_data.get("text", "")
        )
        fr = (
            output_data.finish_reason
            if hasattr(output_data, "finish_reason")
            else output_data.get("finish_reason", "")
        )
        full_content.append(text)
        chunks.append(
            StreamChunk(
                content=text,
                index=len(chunks),
                finish_reason=fr or None,
                raw_chunk=chunk,
            )
        )
        if fr:
            finish_reason = fr
        usage = chunk.usage if hasattr(chunk, "usage") else chunk.get("usage", {})
        if usage:
            input_tokens = getattr(usage, "input_tokens", 0) or usage.get(
                "input_tokens", 0
            )
            output_tokens = getattr(usage, "output_tokens", 0) or usage.get(
                "output_tokens", 0
            )
            total_tokens = getattr(usage, "total_tokens", 0) or usage.get(
                "total_tokens", 0
            )

    return StreamedResponse(
        content="".join(full_content),
        model_id=model_id,
        request_id=request_id,
        finish_reason=finish_reason,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        chunks=chunks,
        raw_response=response,
        metadata={
            "model": model_id,
            "request_id": request_id,
            "chunk_count": len(chunks),
        },
    )
