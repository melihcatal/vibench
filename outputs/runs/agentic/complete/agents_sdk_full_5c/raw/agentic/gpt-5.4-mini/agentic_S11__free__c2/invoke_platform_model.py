import os
from typing import Any, Dict, Optional

from openai import OpenAI

from model_client import get_openai_client, get_model_name
from model_models import ModelRequest, ModelResponse, normalize_text


def invoke_platform_model(prompt: str, *, metadata: Optional[Dict[str, Any]] = None) -> ModelResponse:
    request = ModelRequest(prompt=prompt, metadata=metadata or {})
    client = get_openai_client()
    model = get_model_name(default="gpt-4.1-mini")

    completion = client.responses.create(
        model=model,
        input=request.prompt,
    )

    text = normalize_text(getattr(completion, "output_text", None) or "")
    return ModelResponse(
        text=text,
        provider="openai",
        model=model,
        raw=completion,
    )


if __name__ == "__main__":
    prompt = os.environ.get("MODEL_PROMPT", "Summarize the managed platform workflow.")
    result = invoke_platform_model(prompt)
    print(result.text)
