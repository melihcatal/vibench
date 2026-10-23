from typing import TypedDict, List, Optional, Dict, Any


class ChatMessage(TypedDict):
    role: str
    content: str


class ChatUsage(TypedDict):
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]


class PlatformMetadata(TypedDict):
    content: str
    model: str
    usage: Optional[ChatUsage]
    resource_id: str
    finish_reason: Optional[str]


def normalize_messages(prompt: str) -> List[Dict[str, str]]:
    """
    Normalization helper for chat messages.
    """
    return [{"role": "user", "content": prompt}]
