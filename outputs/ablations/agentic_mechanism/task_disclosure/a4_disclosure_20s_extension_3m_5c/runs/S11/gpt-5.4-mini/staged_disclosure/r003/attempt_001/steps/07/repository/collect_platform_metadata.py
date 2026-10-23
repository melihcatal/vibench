import os
from typing import Any, Dict

from openai import OpenAI


def collect_platform_metadata(prompt: str, model: str = "gpt-5.4-mini") -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(model=model, input=prompt)
    output_text = getattr(response, "output_text", None)
    if output_text is None:
        chunks = []
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                text = getattr(content, "text", None)
                if text:
                    chunks.append(text)
        output_text = "".join(chunks)
    usage = getattr(response, "usage", None)
    metadata = {
        "provider": "openai",
        "model": model,
        "model_handle": getattr(response, "model", model),
        "resource_id": getattr(response, "id", None),
        "usage": {
            "input_tokens": getattr(usage, "input_tokens", None) if usage else None,
            "output_tokens": getattr(usage, "output_tokens", None) if usage else None,
            "total_tokens": getattr(usage, "total_tokens", None) if usage else None,
        },
    }
    return {"output": output_text, "metadata": metadata}
