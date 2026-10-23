import os
from openai import OpenAI
from speech_models import TranscriptionResult, extract_segments_for_translation


def embed_transcript_segments(
    transcript_result: TranscriptionResult,
    openai_api_key: str | None = None,
    model: str = "text-embedding-3-small",
    dimensions: int | None = None,
) -> list[dict]:
    api_key = openai_api_key or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    segments = extract_segments_for_translation(transcript_result)
    embeddings_result = []

    for segment in segments:
        if not segment["text"].strip():
            embeddings_result.append(
                {
                    "segment_id": segment["segment_id"],
                    "speaker": segment["speaker"],
                    "text": segment["text"],
                    "embedding": [],
                    "model": model,
                    "start_ms": segment["start_ms"],
                    "end_ms": segment["end_ms"],
                }
            )
            continue

        kwargs = {
            "input": segment["text"],
            "model": model,
        }
        if dimensions is not None:
            kwargs["dimensions"] = dimensions

        response = client.embeddings.create(**kwargs)

        embedding = response.data[0].embedding

        embeddings_result.append(
            {
                "segment_id": segment["segment_id"],
                "speaker": segment["speaker"],
                "text": segment["text"],
                "embedding": embedding,
                "model": model,
                "usage_tokens": response.usage.total_tokens,
                "start_ms": segment["start_ms"],
                "end_ms": segment["end_ms"],
            }
        )

    return embeddings_result


def embed_full_transcript(
    transcript_result: TranscriptionResult,
    openai_api_key: str | None = None,
    model: str = "text-embedding-3-small",
    dimensions: int | None = None,
) -> dict:
    api_key = openai_api_key or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    text = transcript_result.text
    if not text.strip():
        return {
            "transcription_id": transcript_result.transcription_id,
            "embedding": [],
            "model": model,
        }

    kwargs = {
        "input": text,
        "model": model,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    return {
        "transcription_id": transcript_result.transcription_id,
        "embedding": response.data[0].embedding,
        "model": model,
        "usage_tokens": response.usage.total_tokens,
    }


if __name__ == "__main__":
    from speech_models import TranscriptionResult, TranscriptionStatus, UtteranceInfo

    sample = TranscriptionResult(
        transcription_id="test-embed",
        status=TranscriptionStatus.COMPLETED,
        text="Welcome to the quarterly review meeting.",
        utterances=[
            UtteranceInfo(
                text="Welcome to the quarterly review meeting.",
                speaker="0",
                start_ms=0,
                end_ms=4000,
            ),
        ],
    )
    results = embed_transcript_segments(sample)
    for r in results:
        print(f"Segment {r['segment_id']}: embedding dim={len(r['embedding'])}")
