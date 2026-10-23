import asyncio
import os
from dataclasses import dataclass, field
from typing import AsyncGenerator, List, Optional

import openai

from speech_models import StreamingTranscriptEvent

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


@dataclass
class CaptionEmbedding:
    text: str
    embedding: List[float]
    timestamp: str = ""
    chunk_index: int = 0
    is_final: bool = False


class CaptionEmbedder:
    def __init__(
        self,
        model: str = OPENAI_EMBEDDING_MODEL,
        api_key: Optional[str] = None,
        batch_size: int = 10,
    ):
        self.model = model
        self.batch_size = batch_size
        api_key = api_key or os.environ.get(OPENAI_API_KEY_ENV, "")
        self._client = openai.AsyncOpenAI(api_key=api_key)
        self._embeddings: List[CaptionEmbedding] = []
        self._chunk_index = 0

    async def embed_text(self, text: str) -> List[float]:
        if not text or not text.strip():
            return []

        response = await self._client.embeddings.create(
            model=self.model,
            input=text.strip(),
            encoding_format="float",
        )

        return response.data[0].embedding

    async def embed_event(self, event: StreamingTranscriptEvent) -> CaptionEmbedding:
        self._chunk_index += 1
        embedding = await self.embed_text(event.text)
        caption_embedding = CaptionEmbedding(
            text=event.text,
            embedding=embedding,
            timestamp=event.timestamp.isoformat(),
            chunk_index=self._chunk_index,
            is_final=event.result.is_final,
        )
        self._embeddings.append(caption_embedding)
        return caption_embedding

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []

        response = await self._client.embeddings.create(
            model=self.model,
            input=[t.strip() for t in texts if t.strip()],
            encoding_format="float",
        )

        return [data.embedding for data in response.data]

    def search_similar(
        self, query_embedding: List[float], top_k: int = 5
    ) -> List[dict]:
        if not self._embeddings or not query_embedding:
            return []

        def cosine_similarity(a: List[float], b: List[float]) -> float:
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x * x for x in a) ** 0.5
            norm_b = sum(x * x for x in b) ** 0.5
            if norm_a == 0 or norm_b == 0:
                return 0.0
            return dot / (norm_a * norm_b)

        scored = []
        for emb in self._embeddings:
            if emb.embedding:
                similarity = cosine_similarity(query_embedding, emb.embedding)
                scored.append(
                    {
                        "text": emb.text,
                        "similarity": similarity,
                        "timestamp": emb.timestamp,
                        "chunk_index": emb.chunk_index,
                    }
                )

        scored.sort(key=lambda x: x["similarity"], reverse=True)
        return scored[:top_k]

    def get_all_embeddings(self) -> List[CaptionEmbedding]:
        return list(self._embeddings)

    def reset(self):
        self._embeddings.clear()
        self._chunk_index = 0


async def caption_embedding(
    transcript_events: AsyncGenerator[StreamingTranscriptEvent, None],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> AsyncGenerator[CaptionEmbedding, None]:
    embedder = CaptionEmbedder(model=model)

    async for event in transcript_events:
        if event.text:
            result = await embedder.embed_event(event)
            yield result


async def embed_and_search(
    transcript_events: AsyncGenerator[StreamingTranscriptEvent, None],
    query: str,
    top_k: int = 5,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[dict]:
    embedder = CaptionEmbedder(model=model)

    async for event in transcript_events:
        if event.text:
            await embedder.embed_event(event)

    query_embedding = await embedder.embed_text(query)
    return embedder.search_similar(query_embedding, top_k=top_k)
