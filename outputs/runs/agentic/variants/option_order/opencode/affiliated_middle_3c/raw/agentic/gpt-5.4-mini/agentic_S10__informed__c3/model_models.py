from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TextRequest:
    text: str
    instruction: Optional[str] = None
    context: Optional[str] = None


@dataclass
class JsonExtractionRequest:
    text: str
    schema_hint: Optional[str] = None


@dataclass
class ModelResponse:
    text: str
    raw: Any


def normalize_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and "text" in value:
        return str(value["text"])
    return str(value)


def normalize_json_output(text: str) -> Dict[str, Any]:
    import json

    return json.loads(text)


def messages_from_request(request: TextRequest) -> List[Dict[str, str]]:
    messages = []
    if request.instruction:
        messages.append({"role": "system", "content": request.instruction})
    if request.context:
        messages.append({"role": "user", "content": f"Context:\n{request.context}"})
    messages.append({"role": "user", "content": request.text})
    return messages
