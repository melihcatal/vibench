import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


class ModerationReasonEmbedder:
    def __init__(self, api_key: str | None = None, model: str = DEFAULT_EMBEDDING_MODEL):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def embed_reason(self, reason: str) -> List[float]:
        if not reason or not reason.strip():
            raise ValueError("reason must be a non-empty string")
        response = self.client.embeddings.create(model=self.model, input=reason.strip())
        return list(response.data[0].embedding)

    def embed_reasons(self, reasons: Sequence[str]) -> List[List[float]]:
        cleaned = [reason.strip() for reason in reasons if reason and reason.strip()]
        if not cleaned:
            return []
        response = self.client.embeddings.create(model=self.model, input=cleaned)
        return [list(item.embedding) for item in response.data]


def embed_moderation_reason(reason: str, api_key: str | None = None, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    return ModerationReasonEmbedder(api_key=api_key, model=model).embed_reason(reason)


def embed_moderation_reasons(reasons: Iterable[str], api_key: str | None = None, model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    return ModerationReasonEmbedder(api_key=api_key, model=model).embed_reasons(list(reasons))
