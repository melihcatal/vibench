import os
from typing import Iterable, List, Sequence

from openai import OpenAI


MODEL_ID = "text-embedding-3-small"


class ModerationReasonEmbedder:
    def __init__(self, api_key: str | None = None, model: str = MODEL_ID) -> None:
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def embed_reasons(self, reasons: Sequence[str]) -> List[List[float]]:
        cleaned = [reason.strip() for reason in reasons if reason and reason.strip()]
        if not cleaned:
            return []
        response = self.client.embeddings.create(model=self.model, input=cleaned)
        return [item.embedding for item in response.data]

    def embed_reason(self, reason: str) -> List[float]:
        embeddings = self.embed_reasons([reason])
        return embeddings[0] if embeddings else []


def embed_moderation_rationales(reasons: Iterable[str]) -> List[List[float]]:
    return ModerationReasonEmbedder().embed_reasons(list(reasons))
