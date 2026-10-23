import os
from openai import OpenAI
from speech_models import EmbeddingRequest, EmbeddingResult


def embed_transcript_segments(
    segments: list,
    model: str = "text-embedding-3-small",
) -> EmbeddingResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    texts = []
    for seg in segments:
        if isinstance(seg, dict):
            texts.append(seg.get("text", seg.get("original", "")))
        else:
            texts.append(str(seg))

    response = client.embeddings.create(
        model=model,
        input=texts,
    )

    embeddings = [item.embedding for item in response.data]

    return EmbeddingResult(
        segments=texts,
        embeddings=embeddings,
        model=model,
    )


def build_segment_index(segments: list, model: str = "text-embedding-3-small") -> list:
    result = embed_transcript_segments(segments, model=model)
    index = []
    for i, (seg, emb) in enumerate(zip(result.segments, result.embeddings)):
        index.append(
            {
                "index": i,
                "segment": seg,
                "embedding": emb,
                "model": result.model,
            }
        )
    return index


if __name__ == "__main__":
    sample_segments = [
        {"text": "Welcome to the meeting, let us begin with the agenda."},
        {"text": "The first topic is the quarterly revenue review."},
        {"text": "We need to discuss the new product launch timeline."},
    ]
    index = build_segment_index(sample_segments)
    for entry in index:
        print(
            f"Segment {entry['index']}: {entry['segment'][:50]}... (embedding dim: {len(entry['embedding'])})"
        )
