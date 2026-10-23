import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TextRequest:
    text: str
    context: Optional[str] = None
    question: Optional[str] = None
    schema_hint: Optional[Dict[str, Any]] = None


@dataclass
class TextResponse:
    text: str
    raw: Any = None


def normalize_messages(system: str, user: str) -> List[Dict[str, Any]]:
    return [
        {"role": "user", "content": [{"type": "text", "text": system + "\n\n" + user}]},
    ]


def parse_text_from_bedrock_response(response_body: Dict[str, Any]) -> str:
    if "content" in response_body and response_body["content"]:
        parts = []
        for chunk in response_body["content"]:
            if isinstance(chunk, dict) and chunk.get("type") == "text":
                parts.append(chunk.get("text", ""))
        if parts:
            return "".join(parts)
    if "outputText" in response_body:
        return response_body.get("outputText", "")
    if "completion" in response_body:
        return response_body.get("completion", "")
    return json.dumps(response_body)
