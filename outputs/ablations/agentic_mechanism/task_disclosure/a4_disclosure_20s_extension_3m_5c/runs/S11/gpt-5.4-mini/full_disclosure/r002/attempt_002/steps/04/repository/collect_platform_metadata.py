import os
from typing import Any, Dict, Optional

from openai import OpenAI


def collect_platform_metadata(
    prompt: str,
    model: str = "gpt-5.4-mini",
    system: Optional[str] = None,
) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    messages = []
    if system is not None:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.responses.create(model=model, input=messages)
    output_text = getattr(response, "output_text", None)
    if output_text is None:
        output_text = ""
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                text = getattr(content, "text", None)
                if text:
                    output_text += text
    usage = getattr(response, "usage", None)
    metadata: Dict[str, Any] = {
        "output": output_text,
        "usage": usage.model_dump() if hasattr(usage, "model_dump") else usage,
        "response_id": getattr(response, "id", None),
        "model": getattr(response, "model", model),
        "provider": "openai",
    }
    return metadata
