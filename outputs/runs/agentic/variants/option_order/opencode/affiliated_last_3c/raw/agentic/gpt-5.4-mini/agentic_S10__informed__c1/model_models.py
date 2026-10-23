import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class LLMRequest:
    prompt: str
    system: Optional[str] = None
    context: Optional[str] = None
    temperature: float = 0.2
    max_output_tokens: int = 512
    model: Optional[str] = None


@dataclass
class LLMResponse:
    text: str
    model: str
    usage: Optional[Dict[str, Any]] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def extract_json_object(text: str) -> Dict[str, Any]:
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        return {"raw": text}
    try:
        return json.loads(text[start : end + 1])
    except Exception:
        return {"raw": text}


def merge_stream_chunks(chunks: Iterable[str]) -> str:
    return "".join(chunks).strip()
