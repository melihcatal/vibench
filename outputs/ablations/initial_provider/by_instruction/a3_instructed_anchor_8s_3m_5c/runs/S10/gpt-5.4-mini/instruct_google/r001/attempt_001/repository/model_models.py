from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TextRequest:
    text: str
    instruction: Optional[str] = None
    context: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None


@dataclass
class TextResult:
    text: str
    data: Optional[Dict[str, Any]] = None
    segments: Optional[List[str]] = None


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def json_hint(schema: Optional[Dict[str, Any]]) -> str:
    return f"Return valid JSON matching this schema: {schema}" if schema else "Return valid JSON."
