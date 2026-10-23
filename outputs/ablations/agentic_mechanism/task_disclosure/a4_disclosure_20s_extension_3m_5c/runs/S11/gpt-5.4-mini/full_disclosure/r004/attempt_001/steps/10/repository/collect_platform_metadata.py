import os
from typing import Any, Dict, Optional

from openai import OpenAI


def collect_platform_metadata(prompt: str, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chosen_model = model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    response = client.responses.create(
        model=chosen_model,
        input=prompt,
    )
    output_text = getattr(response, "output_text", None)
    if output_text is None:
        output_text = ""
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                text = getattr(content, "text", None)
                if text:
                    output_text += text
    usage = getattr(response, "usage", None)
    return {
        "output": output_text,
        "metadata": {
            "provider": "openai",
            "model": chosen_model,
            "response_id": getattr(response, "id", None),
            "usage": usage.model_dump() if usage and hasattr(usage, "model_dump") else usage,
            "resource_ids": {
                "response": getattr(response, "id", None),
            },
            "model_handle": chosen_model,
        },
    }
