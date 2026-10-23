import os
from typing import Any, Dict, Optional

from openai import OpenAI


def collect_platform_metadata(prompt: str, model: str = "gpt-4.1-mini") -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(model=model, input=prompt)
    return {
        "output": response.output_text,
        "usage": response.usage.model_dump() if response.usage else None,
        "response_id": response.id,
        "model": response.model,
        "provider": "openai",
        "resource_ids": [item.id for item in getattr(response, "output", []) if hasattr(item, "id")],
    }


if __name__ == "__main__":
    import sys

    prompt_text = sys.argv[1] if len(sys.argv) > 1 else "Hello"
    result = collect_platform_metadata(prompt_text)
    print(result)
