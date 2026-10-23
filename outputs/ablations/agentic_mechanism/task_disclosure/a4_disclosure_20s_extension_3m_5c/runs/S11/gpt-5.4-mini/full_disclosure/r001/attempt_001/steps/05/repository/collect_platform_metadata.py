import os
from typing import Any, Dict, Optional

from openai import OpenAI


def collect_platform_metadata(
    prompt: str,
    *,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    chosen_model = model or os.environ.get("OPENAI_MODEL") or "gpt-4.1-mini"
    response = client.responses.create(
        model=chosen_model,
        input=prompt,
        metadata=metadata,
    )
    usage = getattr(response, "usage", None)
    output_text = getattr(response, "output_text", None)
    return {
        "provider": "openai",
        "model": chosen_model,
        "output": output_text,
        "usage": usage,
        "response_id": getattr(response, "id", None),
        "response": response,
    }
