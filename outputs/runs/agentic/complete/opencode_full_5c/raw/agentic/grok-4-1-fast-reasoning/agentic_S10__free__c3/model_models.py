import json
from typing import TypedDict, List, Dict, Any


class Message(TypedDict):
    role: str
    content: str


class ChatRequest(TypedDict):
    model: str
    messages: List[Message]
    max_tokens: int
    temperature: float


def create_user_message(content: str) -> Message:
    return {"role": "user", "content": content}


def parse_json_extraction(content: str) -> Dict[str, Any]:
    try:
        trimmed = content.strip()
        start_idx = trimmed.find("{")
        end_idx = trimmed.rfind("}") + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = trimmed[start_idx:end_idx]
            return json.loads(json_str)
        return {}
    except json.JSONDecodeError:
        return {}
