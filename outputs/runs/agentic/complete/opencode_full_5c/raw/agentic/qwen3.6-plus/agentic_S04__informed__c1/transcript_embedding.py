import os
from dataclasses import dataclass, field
from typing import List, Optional
from openai import OpenAI

from speech_models import TranscriptSegment, TranscriptSegments


@dataclass
class SegmentEmbedding:
    segment_index: int
    speaker: str
    text: str
    embedding: List[float]
    model: str


@dataclass
class EmbeddingCollection:
    embeddings: List[SegmentEmbedding]
    model: str
    total_segments: int
    dimension: int


def embed_transcript_segments(
    segments: TranscriptSegments,
    api_key: str = None,
    model: str = "text-embedding-3-small",
    organization: str = None,
) -> EmbeddingCollection:
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY", "")

    client_kwargs = {"api_key": api_key}
    if organization:
        client_kwargs["organization"] = organization

    client = OpenAI(**client_kwargs)

    texts = [seg.text for seg in segments.segments if seg.text.strip()]
    segment_indices = [seg.index for seg in segments.segments if seg.text.strip()]
    speakers = [seg.speaker for seg in segments.segments if seg.text.strip()]

    if not texts:
        return EmbeddingCollection(
            embeddings=[],
            model=model,
            total_segments=0,
            dimension=0,
        )

    response = client.embeddings.create(
        input=texts,
        model=model,
    )

    embeddings = []
    dimension = 0
    for i, emb_data in enumerate(response.data):
        vec = emb_data.embedding
        if dimension == 0:
            dimension = len(vec)
        embeddings.append(
            SegmentEmbedding(
                segment_index=segment_indices[i],
                speaker=speakers[i],
                text=texts[i],
                embedding=vec,
                model=model,
            )
        )

    return EmbeddingCollection(
        embeddings=embeddings,
        model=model,
        total_segments=len(embeddings),
        dimension=dimension,
    )


if __name__ == "__main__":
    sample = TranscriptSegments(
        segments=[
            TranscriptSegment(
                index=0,
                speaker="Speaker A",
                text="Welcome to the meeting.",
                start_ms=0,
                end_ms=3000,
            ),
            TranscriptSegment(
                index=1,
                speaker="Speaker B",
                text="Thank you for having me.",
                start_ms=3500,
                end_ms=6000,
            ),
        ],
        total_segments=2,
    )
    collection = embed_transcript_segments(sample)
    print(f"Model: {collection.model}")
    print(f"Dimension: {collection.dimension}")
    print(f"Segments embedded: {collection.total_segments}")
