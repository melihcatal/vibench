from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import build_client, model_for_task
from model_models import ChatRequest, normalize_text


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def prompt_safety(text: str, client: Optional[OpenAI] = None) -> str:
    client = client or build_client()
    moderation = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    flagged = any(result.flagged for result in moderation.results)
    if flagged:
        return "unsafe"
    request = ChatRequest(
        task="prompt_safety",
        model=model_for_task("prompt_safety", default="gpt-4.1-mini"),
        system_prompt="Assess whether content is safe and return a brief safety label.",
        user_prompt=text,
    )
    response = client.chat.completions.create(model=request.model, messages=request.messages(), temperature=0)
    return normalize_text(response.choices[0].message.content or "safe")
