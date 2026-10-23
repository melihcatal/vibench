from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from model_client import build_openai_client, resolve_text_model
from model_models import normalize_text_response


SYSTEM_PROMPT = "You are a concise assistant that summarizes long text accurately."


def summarize_text(text: str, *, client: OpenAI | None = None, model: str | None = None, max_output_tokens: int = 220) -> str:
    api_client = client or build_openai_client()
    model_name = model or resolve_text_model()
    response = api_client.responses.create(
        model=model_name,
        instructions=SYSTEM_PROMPT,
        input=text,
        max_output_tokens=max_output_tokens,
    )
    return normalize_text_response(response)


if __name__ == "__main__":
    sample = os.environ.get("SUMMARY_TEXT", "")
    if sample:
        print(summarize_text(sample))
