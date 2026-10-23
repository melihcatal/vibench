import os
from dataclasses import dataclass, field
from typing import AsyncIterator, Dict, List, Optional, Tuple

import openai
from openai import OpenAI

from speech_models import StreamingRecognitionResult


@dataclass
class CaptionEmbedding:
    text: str
    embedding: List[float]
    timestamp_index: int
    result_id: str = ""


class CaptionEmbedder:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "text-embedding-3-small",
        dimensions: int = 1536,
    ):
        self.model = model
        self.dimensions = dimensions
        self._client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1",
        )
        self._embeddings: List[CaptionEmbedding] = []
        self._index = 0

    def embed_text(self, text: str) -> List[float]:
        response = self._client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=self.dimensions,
        )
        return response.data[0].embedding

    def embed_result(self, result: StreamingRecognitionResult) -> CaptionEmbedding:
        embedding = self.embed_text(result.transcript)
        caption_embedding = CaptionEmbedding(
            text=result.transcript,
            embedding=embedding,
            timestamp_index=self._index,
            result_id=f"chunk_{self._index}",
        )
        self._embeddings.append(caption_embedding)
        self._index += 1
        return caption_embedding

    def search_similar(
        self, query: str, top_k: int = 5
    ) -> List[Tuple[CaptionEmbedding, float]]:
        query_embedding = self.embed_text(query)

        results = []
        for caption_emb in self._embeddings:
            similarity = self._cosine_similarity(query_embedding, caption_emb.embedding)
            results.append((caption_emb, similarity))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)


async def embed_caption_stream(
    caption_stream: AsyncIterator[StreamingRecognitionResult],
    api_key: Optional[str] = None,
    model: str = "text-embedding-3-small",
) -> AsyncIterator[CaptionEmbedding]:
    embedder = CaptionEmbedder(api_key=api_key, model=model)

    async for result in caption_stream:
        if result.is_final and result.transcript.strip():
            yield embedder.embed_result(result)


async def build_semantic_index(
    caption_stream: AsyncIterator[StreamingRecognitionResult],
    api_key: Optional[str] = None,
    model: str = "text-embedding-3-small",
) -> CaptionEmbedder:
    embedder = CaptionEmbedder(api_key=api_key, model=model)

    async for result in caption_stream:
        if result.is_final and result.transcript.strip():
            embedder.embed_result(result)

    return embedder
