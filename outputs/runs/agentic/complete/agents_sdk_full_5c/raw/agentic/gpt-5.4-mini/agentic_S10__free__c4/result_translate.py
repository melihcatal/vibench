from __future__ import annotations

import os

from openai import OpenAI

from model_client import build_openai_client, resolve_translation_model
from model_models import normalize_text_response


SYSTEM_PROMPT = "Translate the text faithfully into the target language while preserving tone and meaning."


def translate_result(text: str, target_language: str, *, client: OpenAI | None = None, model: str | None = None) -> str:
    api_client = client or build_openai_client()
    model_name = model or resolve_translation_model()
    response = api_client.responses.create(
        model=model_name,
        instructions=f"{SYSTEM_PROMPT} Target language: {target_language}.",
        input=text,
    )
    return normalize_text_response(response)


if __name__ == "__main__":
    sample = os.environ.get("TRANSLATE_TEXT", "")
    target = os.environ.get("TARGET_LANGUAGE", "")
    if sample and target:
        print(translate_result(sample, target))
