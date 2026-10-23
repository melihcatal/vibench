from typing import Optional
import httpx
from speech_client import (
    OPENAI_API_KEY,
    EMBEDDINGS_ENDPOINT,
    get_headers,
    validate_api_key,
)
from speech_models import (
    SegmentEmbedding,
    TranscriptionResult,
)


def embed_text(
    text: str, model: str = "text-embedding-3-small", dimensions: int = 1536
) -> list:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    response = httpx.post(
        EMBEDDINGS_ENDPOINT,
        headers=get_headers(),
        json={
            "input": text,
            "model": model,
            "dimensions": dimensions,
        },
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()

    return data["data"][0]["embedding"]


def embed_segments(
    segments: list,
    model: str = "text-embedding-3-small",
    dimensions: int = 1536,
) -> list:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    embeddings = []
    for i, seg in enumerate(segments):
        text = seg.text if hasattr(seg, "text") else seg.get("text", "")
        seg_id = seg.id if hasattr(seg, "id") else seg.get("id", i)

        if not text.strip():
            continue

        vector = embed_text(text, model=model, dimensions=dimensions)

        embeddings.append(
            SegmentEmbedding(
                segment_id=seg_id,
                text=text,
                embedding=vector,
                model=model,
                dimensions=dimensions,
            )
        )

    return embeddings


def transcript_embedding(
    transcript: TranscriptionResult,
    model: str = "text-embedding-3-small",
    dimensions: int = 1536,
) -> list:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    segments = transcript.segments if transcript.segments else []

    if not segments and transcript.text:
        segments = [{"text": transcript.text, "id": 0}]

    return embed_segments(
        segments=segments,
        model=model,
        dimensions=dimensions,
    )


def compute_similarity(embedding1: list, embedding2: list) -> float:
    if len(embedding1) != len(embedding2):
        raise ValueError("Embeddings must have the same dimensions")

    dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
    magnitude1 = sum(a * a for a in embedding1) ** 0.5
    magnitude2 = sum(b * b for b in embedding2) ** 0.5

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def find_similar_segments(
    query_text: str,
    embeddings: list,
    top_k: int = 5,
    model: str = "text-embedding-3-small",
    dimensions: int = 1536,
) -> list:
    query_embedding = embed_text(query_text, model=model, dimensions=dimensions)

    scored = []
    for emb in embeddings:
        similarity = compute_similarity(query_embedding, emb.embedding)
        scored.append(
            {
                "segment_id": emb.segment_id,
                "text": emb.text,
                "similarity": similarity,
            }
        )

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) > 1:
        transcript_file = sys.argv[1]
        query = sys.argv[2] if len(sys.argv) > 2 else ""

        with open(transcript_file, "r") as f:
            data = json.load(f)

        transcript = TranscriptionResult(
            text=data.get("text", ""),
            language=data.get("language", ""),
            duration=data.get("duration", 0.0),
            segments=data.get("segments", []),
        )

        embeddings = transcript_embedding(transcript)
        print(f"Generated {len(embeddings)} segment embeddings")

        if query:
            similar = find_similar_segments(query, embeddings)
            print(f"\nTop similar segments to: '{query}'")
            for item in similar:
                print(
                    f"  [{item['segment_id']}] ({item['similarity']:.3f}) {item['text'][:100]}..."
                )
    else:
        print("Usage: python transcript_embedding.py <transcript.json> [query_text]")
