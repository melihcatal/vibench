from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from openai import OpenAI

from embeddings_client import get_chat_model, get_openai_client


@dataclass(frozen=True)
class RetrievalBrief:
    text: str


def retrieval_audio_brief(results: Iterable[str], topic: str) -> RetrievalBrief:
    client: OpenAI = get_openai_client()
    model = get_chat_model()
    prompt = "\n".join([f"Topic: {topic}", "Retrieved results:", *[f"- {item}" for item in results]])
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Write a short spoken brief suitable for text-to-speech."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return RetrievalBrief(text=response.choices[0].message.content or "")
