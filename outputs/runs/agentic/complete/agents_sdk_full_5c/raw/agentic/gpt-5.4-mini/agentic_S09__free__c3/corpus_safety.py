from __future__ import annotations

from openai import OpenAI

from embeddings_client import load_settings


def corpus_safety(texts: list[str]) -> dict[str, object]:
    settings = load_settings()
    client = OpenAI()
    verdicts: list[dict[str, object]] = []
    for text in texts:
        moderation = client.moderations.create(model="omni-moderation-latest", input=text)
        verdicts.append(
            {
                "text": text,
                "flagged": moderation.results[0].flagged,
                "categories": moderation.results[0].categories.model_dump(),
            }
        )
    return {"provider": "openai", "model": settings.embedding_model, "verdicts": verdicts}
