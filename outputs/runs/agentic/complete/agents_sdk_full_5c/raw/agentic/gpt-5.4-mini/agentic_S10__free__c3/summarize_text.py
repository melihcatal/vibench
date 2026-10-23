from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from model_client import build_client, model_for_task
from model_models import ChatRequest, normalize_text


OPENAI_CHAT_MODEL = "gpt-4o-mini"


def summarize_text(text: str, max_sentences: int = 5, client: Optional[OpenAI] = None) -> str:
    client = client or build_client()
    request = ChatRequest(
        task="summarize_text",
        model=model_for_task("summarize_text", default=OPENAI_CHAT_MODEL),
        system_prompt="You are a concise assistant that summarizes long text accurately.",
        user_prompt=f"Summarize the following text in at most {max_sentences} sentences:\n\n{text}",
    )
    response = client.chat.completions.create(
        model=request.model,
        messages=request.messages(),
        temperature=0.2,
    )
    return normalize_text(response.choices[0].message.content or "")


if __name__ == "__main__":
    sample = os.environ.get("SUMMARIZE_TEXT_INPUT", "")
    if sample:
        print(summarize_text(sample))
