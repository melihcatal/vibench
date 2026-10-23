from typing import TypedDict, List, Dict, Any

class PlatformMessage(TypedDict):
    role: str
    content: str

def normalize_request(model: str, messages: List[dict], **kwargs) -> Dict[str, Any]:
    norm_messages = [{"role": msg["role"], "content": msg.get("content", "")} for msg in messages]
    return {
        "model": model,
        "messages": norm_messages,
        **kwargs
    }
