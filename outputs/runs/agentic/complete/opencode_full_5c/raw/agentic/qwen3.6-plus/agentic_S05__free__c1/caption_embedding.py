import os
from typing import AsyncIterator
from datetime import datetime

from vertexai.language_models import TextEmbeddingModel

from speech_models import StreamingResult, StreamingEvent


class CaptionEmbedder:
    def __init__(
        self,
        model_name: str = "text-embedding-005",
        project_id: str | None = None,
        location: str = "us-central1",
        dimensionality: int = 768,
    ):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT", "")
        self.location = location
        self.model_name = model_name
        self.dimensionality = dimensionality
        self._embeddings: list[dict] = []

        import vertexai

        vertexai.init(project=self.project_id, location=self.location)
        self._model = TextEmbeddingModel.from_pretrained(self.model_name)

    def embed_text(self, text: str) -> list[float]:
        if not text.strip():
            return []
        result = self._model.get_embeddings(
            [text],
            output_dimensionality=self.dimensionality,
        )
        return result[0].values if result else []

    def embed_event(self, event: StreamingEvent) -> dict:
        if event.result is None or not event.result.transcript.strip():
            return {
                "event_type": event.event_type,
                "transcript": "",
                "embedding": [],
                "timestamp": event.result.timestamp.isoformat()
                if event.result and event.result.timestamp
                else datetime.utcnow().isoformat(),
                "chunk_index": event.result.chunk_index if event.result else 0,
            }

        embedding = self.embed_text(event.result.transcript)
        embedding_record = {
            "event_type": event.event_type,
            "transcript": event.result.transcript,
            "embedding": embedding,
            "timestamp": event.result.timestamp.isoformat()
            if event.result.timestamp
            else datetime.utcnow().isoformat(),
            "chunk_index": event.result.chunk_index,
            "language_code": event.result.language_code,
            "is_final": event.result.is_final,
        }
        self._embeddings.append(embedding_record)
        return embedding_record

    def search_similar(self, query: str, top_k: int = 5) -> list[dict]:
        query_embedding = self.embed_text(query)
        if not query_embedding or not self._embeddings:
            return []

        scored = []
        for record in self._embeddings:
            emb = record.get("embedding", [])
            if len(emb) != len(query_embedding):
                continue
            dot_product = sum(a * b for a, b in zip(query_embedding, emb))
            mag_q = sum(a * a for a in query_embedding) ** 0.5
            mag_e = sum(a * a for a in emb) ** 0.5
            if mag_q > 0 and mag_e > 0:
                similarity = dot_product / (mag_q * mag_e)
                scored.append((similarity, record))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"similarity": score, **record} for score, record in scored[:top_k]]


async def caption_embedding(
    transcript_events: AsyncIterator[StreamingEvent],
    model_name: str = "text-embedding-005",
    project_id: str | None = None,
    location: str = "us-central1",
    dimensionality: int = 768,
) -> AsyncIterator[dict]:
    embedder = CaptionEmbedder(
        model_name=model_name,
        project_id=project_id,
        location=location,
        dimensionality=dimensionality,
    )
    async for event in transcript_events:
        if event.result and event.result.transcript.strip():
            embedding_record = embedder.embed_event(event)
            yield embedding_record
