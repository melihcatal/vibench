import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TextRequest:
    text: str
    instruction: Optional[str] = None


@dataclass
class QARequest:
    context: str
    question: str


@dataclass
class JsonRequest:
    text: str
    schema_hint: Optional[str] = None


def normalize_text_output(raw: Any) -> str:
    if isinstance(raw, dict):
        if "content" in raw and raw["content"]:
            item = raw["content"][0]
            if isinstance(item, dict) and "text" in item:
                return item["text"]
        for key in ("outputText", "completion", "text"):
            if key in raw:
                return raw[key]
    return str(raw)


def parse_json_output(text: str) -> Dict[str, Any]:
    return json.loads(text)
