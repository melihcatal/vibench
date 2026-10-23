from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from embeddings_client import get_openai_client


MODERATION_MODEL = "omni-moderation-latest"


def corpus_safety(texts: Iterable[str], model: str = MODERATION_MODEL) -> dict[str, object]:
    corpus = [text for text in texts if text and text.strip()]
    if not corpus:
        return {"flagged": False, "results": []}

    client: OpenAI = get_openai_client()
    response = client.moderations.create(model=model, input=corpus)
    payload = response.model_dump()
    flagged = any(result.get("flagged", False) for result in payload.get("results", []))
    return {"flagged": flagged, "results": payload.get("results", [])}
