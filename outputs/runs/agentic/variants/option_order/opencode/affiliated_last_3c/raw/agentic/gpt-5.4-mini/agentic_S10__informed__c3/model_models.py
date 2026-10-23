from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LLMRequest:
    prompt: str
    system: str = ""
    temperature: float = 0.2
    model: str = ""


@dataclass
class LLMResponse:
    text: str
    model: str
    raw: Any = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def normalize_json_text(text: str) -> str:
    return text.strip()


def normalize_embedding(values: List[float]) -> Dict[str, Any]:
    return {"embedding": values, "dimension": len(values)}
