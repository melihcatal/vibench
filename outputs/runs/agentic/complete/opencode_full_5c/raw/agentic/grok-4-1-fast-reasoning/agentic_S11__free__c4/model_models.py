from typing import List, Dict, Any

ChatMessages = List[Dict[str, str]]


def normalize_request(
    messages: ChatMessages, max_tokens: int = 1024, temperature: float = 0.7, **kwargs
) -> Dict[str, Any]:
    return {
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        **kwargs,
    }
