import hashlib
from typing import Optional

import httpx

from speech_client import ASSEMBLYAI_API_BASE, build_headers, get_transcription_result
from speech_models import (
    EmbeddingRequest,
    SegmentEmbedding,
    TranscriptionResult,
)


def generate_embedding(text: str, model: str = "all-MiniLM-L6-v2") -> list[float]:
    api_key_headers = build_headers()
    response = httpx.post(
        f"{ASSEMBLYAI_API_BASE}/embeddings",
        headers=api_key_headers,
        json={"text": text, "model": model},
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()["embedding"]


def embed_transcript_segments(
    transcript_id: str,
    chunk_size: int = 512,
    overlap: int = 50,
) -> list[SegmentEmbedding]:
    response = get_transcription_result(transcript_id)
    result = TranscriptionResult.from_assemblyai_response(response)

    request = EmbeddingRequest(
        transcript_id=transcript_id,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    segments = request.to_segments(result)
    embeddings = []

    for i, segment in enumerate(segments):
        embedding = generate_embedding(segment["text"])
        segment_embedding = SegmentEmbedding.from_segment(
            segment=segment,
            embedding=embedding,
            index=i,
        )
        embeddings.append(segment_embedding)

    return embeddings


def compute_segment_hash(segment: SegmentEmbedding) -> str:
    content = f"{segment.speaker}:{segment.start_ms}:{segment.text}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def build_embedding_index(
    embeddings: list[SegmentEmbedding],
) -> dict[str, dict]:
    index = {}
    for emb in embeddings:
        seg_hash = compute_segment_hash(emb)
        index[seg_hash] = {
            "segment_index": emb.segment_index,
            "speaker": emb.speaker,
            "text": emb.text,
            "start_ms": emb.start_ms,
            "end_ms": emb.end_ms,
            "embedding": emb.embedding,
        }
    return index


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def search_similar_segments(
    query_embedding: list[float],
    index: dict[str, dict],
    top_k: int = 5,
) -> list[tuple[str, float]]:
    scores = []
    for seg_hash, seg_data in index.items():
        similarity = cosine_similarity(query_embedding, seg_data["embedding"])
        scores.append((seg_hash, similarity))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]
