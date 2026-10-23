from typing import Any, Dict

from openai import OpenAI

from model_client import get_openai_client, get_model_name
from model_models import ModelResponse, normalize_text


def collect_platform_metadata(prompt: str) -> Dict[str, Any]:
    client: OpenAI = get_openai_client()
    model = get_model_name(default="gpt-4.1-mini")
    completion = client.responses.create(model=model, input=prompt)

    text = normalize_text(getattr(completion, "output_text", None) or "")
    usage = getattr(completion, "usage", None)
    return {
        "response": ModelResponse(text=text, provider="openai", model=model, raw=completion),
        "usage": usage,
        "model": model,
        "response_id": getattr(completion, "id", None),
    }
