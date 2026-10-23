from dataclasses import asdict
from openai.types.chat.chat_completion import ChatCompletion
from typing import Any


def collect_platform_metadata(response: ChatCompletion) -> dict[str, Any]:
    choice = response.choices[0]
    usage = asdict(response.usage) if response.usage else {}
    return {
        "output": choice.message.content or "",
        "usage": usage,
        "model": response.model,
        "id": response.id,
        "created": response.created,
        "system_fingerprint": getattr(response, "system_fingerprint", None),
        "finish_reason": choice.finish_reason,
    }
