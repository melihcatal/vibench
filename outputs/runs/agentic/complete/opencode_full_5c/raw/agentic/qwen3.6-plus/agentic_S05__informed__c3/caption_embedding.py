from __future__ import annotations

import os
import logging
from collections.abc import AsyncGenerator

from openai import AsyncOpenAI

from speech_models import TranscriptResult, StreamingEvent

logger = logging.getLogger(__name__)

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def create_openai_client(api_key: str | None = None) -> AsyncOpenAI:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return AsyncOpenAI(api_key=key)


async def embed_caption_chunk(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    client: AsyncOpenAI | None = None,
) -> list[float]:
    if client is None:
        client = create_openai_client()

    response = await client.embeddings.create(
        model=model,
        input=text,
        encoding_format="float",
    )

    if response.data:
        return response.data[0].embedding
    return []


async def embed_caption_stream(
    source: AsyncGenerator[StreamingEvent, None],
    model: str = OPENAI_EMBEDDING_MODEL,
    client: AsyncOpenAI | None = None,
) -> AsyncGenerator[StreamingEvent, None]:
    if client is None:
        client = create_openai_client()

    async for event in source:
        if event.result is None or not event.result.text.strip():
            yield event
            continue

        try:
            embedding = await embed_caption_chunk(
                text=event.result.text,
                model=model,
                client=client,
            )

            if event.raw_payload is None:
                event.raw_payload = {}
            event.raw_payload["embedding"] = {
                "model": model,
                "vector": embedding,
                "dimension": len(embedding),
            }

            yield event
        except Exception as exc:
            logger.error("OpenAI embedding error: %s", exc)
            yield event


class CaptionEmbeddingStore:
    def __init__(
        self,
        model: str = OPENAI_EMBEDDING_MODEL,
        client: AsyncOpenAI | None = None,
    ):
        self.model = model
        self.client = client or create_openai_client()
        self._entries: list[dict] = []

    async def add_entry(
        self,
        text: str,
        timestamp: float | None = None,
        metadata: dict | None = None,
    ) -> dict:
        embedding = await embed_caption_chunk(
            text=text,
            model=self.model,
            client=self.client,
        )

        entry = {
            "text": text,
            "embedding": embedding,
            "timestamp": timestamp,
            "metadata": metadata or {},
        }
        self._entries.append(entry)
        return entry

    async def add_from_stream(
        self,
        source: AsyncGenerator[StreamingEvent, None],
    ) -> AsyncGenerator[dict, None]:
        async for event in source:
            if event.result is None or not event.result.text.strip():
                continue

            entry = await self.add_entry(
                text=event.result.text,
                timestamp=event.result.timestamp,
                metadata={"is_final": event.result.is_final},
            )
            yield entry

    def search_similar(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        if not self._entries:
            return []

        scores = []
        for entry in self._entries:
            similarity = _cosine_similarity(query_embedding, entry["embedding"])
            scores.append((similarity, entry))

        scores.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in scores[:top_k]]

    @property
    def entries(self) -> list[dict]:
        return list(self._entries)

    @property
    def count(self) -> int:
        return len(self._entries)


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        return 0.0

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)
