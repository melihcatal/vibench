import os
from typing import Any, Dict

from openai import OpenAI


def collect_platform_metadata(prompt: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )
    return {
        "output": response.output_text,
        "metadata": {
            "provider": "openai",
            "model": response.model,
            "response_id": response.id,
            "usage": response.usage.model_dump() if response.usage is not None else None,
        },
    }
