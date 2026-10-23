"""Embed caption chunks for semantic meeting search using Google Cloud Vertex AI Embeddings."""

import json
from typing import List, Optional, Tuple

from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

from speech_models import TranscriptSegment, StreamingSpeechEvent


class CaptionEmbedder:
    """Embeds caption chunks using Google Cloud Vertex AI Text Embedding model for semantic search.

    Uses vertexai.language_models.TextEmbeddingModel with 'textembedding-gecko@003'
    to generate dense vector embeddings for meeting caption segments.
    """

    EMBEDDING_MODEL_NAME = "textembedding-gecko@003"

    def __init__(
        self,
        project: Optional[str] = None,
        location: str = "us-central1",
        dimensionality: int = 768,
    ):
        """Initialize the Google Cloud Vertex AI text embedder.

        Uses vertexai.language_models.TextEmbeddingModel with the
        textembedding-gecko@003 model on Google Cloud Vertex AI.
        """
        self.project = project
        self.location = location
        self.dimensionality = dimensionality

        aiplatform.init(project=self.project, location=self.location)
        self.embedding_model = TextEmbeddingModel.from_pretrained(
            self.EMBEDDING_MODEL_NAME
        )

    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string using Google Cloud Vertex AI textembedding-gecko@003.

        Returns a list of floats representing the dense embedding vector.
        """
        if not text.strip():
            return []

        embeddings = self.embedding_model.get_embeddings(
            texts=[text],
        )

        if embeddings and embeddings[0].values:
            return embeddings[0].values

        return []

    def embed_segment(self, segment: TranscriptSegment) -> Tuple[TranscriptSegment, List[float]]:
        """Embed a single TranscriptSegment via Google Cloud Vertex AI textembedding-gecko@003.

        Returns a tuple of (segment, embedding_vector).
        """
        embedding = self.embed_text(segment.text)
        return segment, embedding

    def embed_event(self, event: StreamingSpeechEvent) -> List[Tuple[TranscriptSegment, List[float]]]:
        """Embed all segments in a StreamingSpeechEvent.

        Uses Google Cloud Vertex AI textembedding-gecko@003 model to generate
        embeddings for each caption segment in the event.
        """
        if event.error:
            return []

        results = []
        for segment in event.segments:
            if segment.text.strip():
                segment, embedding = self.embed_segment(segment)
                results.append((segment, embedding))
        return results

    def embed_stream(
        self,
        events: List[StreamingSpeechEvent],
    ) -> List[Tuple[TranscriptSegment, List[float]]]:
        """Embed an entire stream of streaming speech events.

        Processes Google Cloud Speech-to-Text events and returns
        (TranscriptSegment, embedding) tuples for semantic search indexing.
        """
        all_embeddings = []
        for event in events:
            event_embeddings = self.embed_event(event)
            all_embeddings.extend(event_embeddings)
        return all_embeddings

    def build_search_index(
        self,
        events: List[StreamingSpeechEvent],
    ) -> List[dict]:
        """Build a semantic search index from caption events.

        Returns a list of dicts with text, timestamp metadata, and embedding vectors
        suitable for vector similarity search in Google Cloud Vertex AI Vector Search.
        """
        indexed = []
        segment_index = 0

        for event in events:
            for segment in event.segments:
                if not segment.text.strip():
                    continue
                embedding = self.embed_text(segment.text)
                indexed.append(
                    {
                        "segment_id": segment_index,
                        "text": segment.text,
                        "is_final": segment.is_final,
                        "confidence": segment.confidence,
                        "stability": segment.stability,
                        "language_code": segment.language_code,
                        "embedding": embedding,
                        "dimensionality": self.dimensionality,
                    }
                )
                segment_index += 1

        return indexed

    def search_semantic(
        self,
        query: str,
        index: List[dict],
        top_k: int = 5,
    ) -> List[dict]:
        """Perform semantic similarity search over caption embeddings.

        Embeds the query with Google Cloud Vertex AI textembedding-gecko@003,
        then performs cosine similarity against the pre-built index.
        """
        query_embedding = self.embed_text(query)
        if not query_embedding:
            return []

        results = []
        for item in index:
            score = _cosine_similarity(query_embedding, item["embedding"])
            results.append((score, item))

        results.sort(key=lambda x: x[0], reverse=True)
        return [
            {"score": score, **item}
            for score, item in results[:top_k]
        ]


def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Used for ranking caption chunks against query embeddings from
    Google Cloud Vertex AI textembedding-gecko@003.
    """
    if not vec_a or not vec_b:
        return 0.0

    min_len = min(len(vec_a), len(vec_b))
    dot_product = sum(a * b for a, b in zip(vec_a[:min_len], vec_b[:min_len]))
    norm_a = sum(a * a for a in vec_a[:min_len]) ** 0.5
    norm_b = sum(b * b for b in vec_b[:min_len]) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


async def embed_captions_async(
    event_stream,
    project: Optional[str] = None,
    location: str = "us-central1",
) -> List[Tuple[TranscriptSegment, List[float]]]:
    """Async helper to embed a stream of caption events via Google Cloud Vertex AI.

    Uses vertexai.language_models.TextEmbeddingModel with textembedding-gecko@003
    to generate embeddings for semantic meeting search.
    """
    import asyncio

    embedder = CaptionEmbedder(project=project, location=location)

    events = []
    async for event in event_stream:
        events.append(event)

    loop = asyncio.get_event_loop()
    embeddings = await loop.run_in_executor(
        None, lambda: embedder.embed_stream(events)
    )

    return embeddings
