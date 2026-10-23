import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class LlmRequest:
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.2
    top_p: float = 0.9


@dataclass(frozen=True)
class LlmResponse:
    text: str
    raw: Dict[str, Any]


def normalize_messages(system: Optional[str], user: str) -> List[Dict[str, str]]:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})
    return messages


def extract_text(raw: Dict[str, Any]) -> str:
    if "outputText" in raw:
        return raw["outputText"]
    if "generation" in raw:
        return raw["generation"]
    if "content" in raw and isinstance(raw["content"], list):
        parts = []
        for item in raw["content"]:
            if isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
        if parts:
            return "".join(parts)
    if "outputs" in raw and isinstance(raw["outputs"], list) and raw["outputs"]:
        first = raw["outputs"][0]
        if isinstance(first, dict) and "text" in first:
            return first["text"]
    return json.dumps(raw)


def parse_json_text(text: str) -> Any:
    return json.loads(text)
