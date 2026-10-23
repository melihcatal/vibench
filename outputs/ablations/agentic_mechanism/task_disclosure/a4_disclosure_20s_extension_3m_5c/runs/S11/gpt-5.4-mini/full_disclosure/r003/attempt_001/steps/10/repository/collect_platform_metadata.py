import os
from typing import Any, Dict, Optional

from openai import OpenAI


def collect_platform_metadata(prompt: str, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model or "gpt-5.4-mini",
        input=prompt,
    )
    output_text = getattr(response, "output_text", None)
    if output_text is None:
        output_text = ""
    usage = getattr(response, "usage", None)
    return {
        "output": output_text,
        "metadata": {
            "provider": "openai",
            "model": getattr(response, "model", model or "gpt-5.4-mini"),
            "response_id": getattr(response, "id", None),
            "usage": usage.model_dump() if hasattr(usage, "model_dump") else usage,
            "resource_ids": getattr(response, "output", None),
            "model_handle": getattr(response, "model", model or "gpt-5.4-mini"),
        },
    }
