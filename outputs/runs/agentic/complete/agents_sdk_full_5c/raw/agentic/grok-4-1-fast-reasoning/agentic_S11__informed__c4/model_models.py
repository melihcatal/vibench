from typing import List, Dict, Any

def build_chat_request(
    messages: List[Dict[str, str]],
    **kwargs: Any
) -> Dict[str, Any]:
    return {
        "messages": messages,
        "max_tokens": kwargs.get("max_tokens", 1000),
        "temperature": kwargs.get("temperature", 0.7),
        **kwargs
    }

def extract_content(response: Any) -> str:
    return response.choices[0].message.content

def extract_usage(response: Any) -> Dict[str, int | None]:
    usage = response.usage
    if usage:
        return {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": getattr(usage, "total_tokens", None),
        }
    return {}
