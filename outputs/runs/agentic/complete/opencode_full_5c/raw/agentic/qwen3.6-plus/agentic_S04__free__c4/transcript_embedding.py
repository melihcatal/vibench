from openai import OpenAI
from speech_client import get_openai_client, OPENAI_EMBEDDING_MODEL
from speech_models import EmbeddingResult, TranscriptSegment


def embed_transcript_segments(
    segments: list[TranscriptSegment], model: str = OPENAI_EMBEDDING_MODEL
) -> list[EmbeddingResult]:
    client: OpenAI = get_openai_client()
    texts = [seg.text for seg in segments]
    response = client.embeddings.create(
        input=texts,
        model=model,
    )
    results = []
    for idx, data in enumerate(response.data):
        results.append(
            EmbeddingResult(
                segment_index=idx,
                text=segments[idx].text,
                embedding=data.embedding,
                model=model,
            )
        )
    return results


def embed_single_segment(
    segment: TranscriptSegment, model: str = OPENAI_EMBEDDING_MODEL
) -> EmbeddingResult:
    client: OpenAI = get_openai_client()
    response = client.embeddings.create(
        input=segment.text,
        model=model,
    )
    return EmbeddingResult(
        segment_index=0,
        text=segment.text,
        embedding=response.data[0].embedding,
        model=model,
    )


def embed_transcript_text(
    text: str, model: str = OPENAI_EMBEDDING_MODEL
) -> list[float]:
    client: OpenAI = get_openai_client()
    response = client.embeddings.create(
        input=text,
        model=model,
    )
    return response.data[0].embedding
