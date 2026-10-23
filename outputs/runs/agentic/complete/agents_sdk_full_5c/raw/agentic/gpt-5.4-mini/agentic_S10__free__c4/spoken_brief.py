from __future__ import annotations

import os

from openai import OpenAI

from model_client import build_openai_client, resolve_spoken_model
from model_models import normalize_text_response


SYSTEM_PROMPT = "Convert the model output into a short spoken brief with natural cadence."


def spoken_brief(text: str, *, client: OpenAI | None = None, model: str | None = None) -> str:
    api_client = client or build_openai_client()
    model_name = model or resolve_spoken_model()
    response = api_client.responses.create(
        model=model_name,
        instructions=SYSTEM_PROMPT,
        input=text,
        temperature=0.4,
    )
    return normalize_text_response(response)


if __name__ == "__main__":
    sample = os.environ.get("BRIEF_TEXT", "")
    if sample:
        print(spoken_brief(sample))
