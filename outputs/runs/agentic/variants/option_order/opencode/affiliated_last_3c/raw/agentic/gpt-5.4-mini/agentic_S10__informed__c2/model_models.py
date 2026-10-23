from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class LLMRequest:
    text: str
    context: Optional[str] = None
    question: Optional[str] = None
    language: Optional[str] = None


@dataclass
class LLMResponse:
    content: str
    model: str


def normalize_messages(*parts: str) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = []
    for part in parts:
        if part:
            messages.append({"role": "user", "content": part})
    return messages


def join_stream(chunks: Iterable[str]) -> str:
    return "".join(chunks)


def as_json_payload(content: str) -> Dict[str, Any]:
    return {"result": content}
