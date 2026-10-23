import os
from typing import Any, Dict, Optional

from openai import OpenAI


def collect_platform_metadata(prompt: str, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_id = model or os.environ.get("OPENAI_MODEL", "gpt-5.4-mini")
    response = client.responses.create(model=model_id, input=prompt)
    return {
        "output": response.output_text,
        "metadata": {
            "provider": "openai",
            "model": response.model,
            "response_id": response.id,
            "usage": response.usage.model_dump() if response.usage else None,
            "resource_ids": [item.get("id") for item in getattr(response, "output", []) if isinstance(item, dict) and item.get("id")],
            "model_handle": getattr(response, "model", model_id),
        },
    }
