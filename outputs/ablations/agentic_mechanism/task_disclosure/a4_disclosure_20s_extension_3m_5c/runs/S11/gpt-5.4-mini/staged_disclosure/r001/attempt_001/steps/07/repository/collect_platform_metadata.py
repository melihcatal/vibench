import os
from typing import Any, Dict, Optional

from openai import OpenAI


def collect_platform_metadata(prompt: str, model: str = "gpt-4.1-mini") -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model,
        input=prompt,
    )
    output_text = getattr(response, "output_text", None)
    if output_text is None:
        output_text = "".join(
            getattr(item, "text", "")
            for item in getattr(response, "output", [])
            for content in getattr(item, "content", [])
            if getattr(content, "type", None) == "output_text"
        )
    usage = getattr(response, "usage", None)
    metadata = {
        "provider": "openai",
        "model": model,
        "response_id": getattr(response, "id", None),
        "output": output_text,
        "usage": {
            "input_tokens": getattr(usage, "input_tokens", None) if usage else None,
            "output_tokens": getattr(usage, "output_tokens", None) if usage else None,
            "total_tokens": getattr(usage, "total_tokens", None) if usage else None,
        },
        "model_handle": getattr(response, "model", None),
    }
    return metadata
