import os
from openai import OpenAI
from speech_models import TranscriptionResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def embed_transcript_segments(
    segments: list[dict],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> list[dict]:
    client = get_openai_client()

    texts = [seg.get("text", "") for seg in segments if seg.get("text", "").strip()]

    if not texts:
        return []

    response = client.embeddings.create(
        input=texts,
        model=model,
    )

    embeddings_with_metadata = []
    text_index = 0
    for seg in segments:
        if seg.get("text", "").strip():
            embedding_data = response.data[text_index]
            embeddings_with_metadata.append(
                {
                    **seg,
                    "embedding": embedding_data.embedding,
                    "embedding_model": model,
                    "embedding_dimensions": len(embedding_data.embedding),
                }
            )
            text_index += 1
        else:
            embeddings_with_metadata.append(
                {
                    **seg,
                    "embedding": None,
                    "embedding_model": model,
                    "embedding_dimensions": 0,
                }
            )

    return embeddings_with_metadata


def embed_full_transcript(
    transcript_result: TranscriptionResult,
    model: str = OPENAI_EMBEDDING_MODEL,
    chunk_size: int = 200,
) -> list[dict]:
    text = transcript_result.text
    words = text.split()

    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk_text = " ".join(words[i : i + chunk_size])
        chunks.append(
            {
                "text": chunk_text,
                "chunk_index": i // chunk_size,
                "transcript_id": transcript_result.transcript_id,
            }
        )

    return embed_transcript_segments(chunks, model=model)


def build_embedding_index(
    transcript_result: TranscriptionResult,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> dict:
    if transcript_result.utterances:
        segments = [
            {
                "text": u.text,
                "speaker": u.speaker,
                "start_ms": u.start,
                "end_ms": u.end,
            }
            for u in transcript_result.utterances
        ]
    else:
        segments = [{"text": transcript_result.text, "speaker": None}]

    embedded = embed_transcript_segments(segments, model=model)

    return {
        "transcript_id": transcript_result.transcript_id,
        "embedding_model": model,
        "segments": embedded,
        "total_segments": len(embedded),
    }


if __name__ == "__main__":
    sample_result = TranscriptionResult(
        transcript_id="test-456",
        status="completed",
        text="The quarterly review covered sales performance, marketing initiatives, "
        "and product development updates. Key metrics showed a fifteen percent increase "
        "in revenue compared to last quarter.",
        confidence=0.92,
        audio_duration=180.0,
        language_code="en",
    )

    index = build_embedding_index(sample_result)
    print(
        f"Embedded {index['total_segments']} segments using {index['embedding_model']}"
    )
