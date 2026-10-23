from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


@dataclass(slots=True)
class ChatRequest:
    system_prompt: str
    user_prompt: str
    model: Optional[str] = None
    temperature: float = 0.2
    max_output_tokens: int = 400


@dataclass(slots=True)
class AnswerRequest:
    question: str
    context: str
    system_prompt: str = "Answer using only the provided context. If the answer is not in the context, say you do not know."
    model: Optional[str] = None
    temperature: float = 0.1
    max_output_tokens: int = 300


@dataclass(slots=True)
class ExtractionRequest:
    instruction: str
    source_text: str
    schema_hint: Mapping[str, Any] = field(default_factory=dict)
    model: Optional[str] = None
    temperature: float = 0.0
    max_output_tokens: int = 500


@dataclass(slots=True)
class GenerationResponse:
    text: str
    model: str
    finish_reason: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)


def trim_text(value: str, limit: int = 12000) -> str:
    value = value.strip()
    if len(value) <= limit:
        return value
    return value[:limit]


def build_messages(system_prompt: str, user_prompt: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": user_prompt.strip()},
    ]


def normalize_text_response(response: Any) -> GenerationResponse:
    output_text = getattr(response, "output_text", "") or ""
    model = getattr(response, "model", "") or ""
    usage_obj = getattr(response, "usage", None)
    usage = usage_obj.model_dump() if hasattr(usage_obj, "model_dump") else {}
    finish_reason = None
    output = getattr(response, "output", None) or []
    for item in output:
        content = getattr(item, "content", None) or []
        for part in content:
            part_finish = getattr(part, "finish_reason", None)
            if part_finish:
                finish_reason = part_finish
                break
        if finish_reason:
            break
    return GenerationResponse(
        text=output_text, model=model, finish_reason=finish_reason, usage=usage
    )
