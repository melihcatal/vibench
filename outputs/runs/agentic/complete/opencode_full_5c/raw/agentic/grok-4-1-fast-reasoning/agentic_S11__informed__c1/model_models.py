from typing import TypedDict, List, Dict, Any


class Message(TypedDict):
    role: str
    content: str


class Usage(TypedDict):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


def normalize_messages(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [{"role": msg["role"], "content": msg["content"]} for msg in messages]
