from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PlatformMessage:
    role: str
    content: str


def normalize_messages(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [{"role": m["role"], "content": m["content"]} for m in messages]


def response_text(response: Any) -> str:
    return response.choices[0].message.content or ""


def response_usage(response: Any) -> Dict[str, Optional[int]]:
    usage = getattr(response, "usage", None)
    return {
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
    }
