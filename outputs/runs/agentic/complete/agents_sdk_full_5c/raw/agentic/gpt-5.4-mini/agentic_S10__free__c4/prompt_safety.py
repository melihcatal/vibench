from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from model_client import build_openai_client, resolve_safety_model


SAFETY_PROMPT = "Flag unsafe, self-harm, hate, sexual, or violent content and return structured moderation labels."


def check_prompt_safety(text: str, *, client: OpenAI | None = None, model: str | None = None) -> dict[str, Any]:
    api_client = client or build_openai_client()
    model_name = model or resolve_safety_model()
    response = api_client.moderations.create(model=model_name, input=text)
    return response.model_dump() if hasattr(response, "model_dump") else {"raw": response}


if __name__ == "__main__":
    sample = os.environ.get("SAFETY_TEXT", "")
    if sample:
        print(check_prompt_safety(sample))
