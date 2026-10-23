from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import build_client, model_for_task
from model_models import ChatRequest, normalize_text


OPENAI_TRANSLATION_MODEL = "gpt-4.1-mini"


def result_translate(text: str, target_language: str, client: Optional[OpenAI] = None) -> str:
    client = client or build_client()
    request = ChatRequest(
        task="result_translate",
        model=model_for_task("result_translate", default=OPENAI_TRANSLATION_MODEL),
        system_prompt="You translate text accurately while preserving meaning.",
        user_prompt=f"Translate the following text into {target_language}:\n\n{text}",
    )
    response = client.chat.completions.create(model=request.model, messages=request.messages(), temperature=0.2)
    return normalize_text(response.choices[0].message.content or "")
