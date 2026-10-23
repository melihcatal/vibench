import io
from speech_client import get_openai_client
from speech_models import (
    TranscriptRequest,
    TranscriptResponse,
    normalize_transcript_request,
)

OPENAI_WHISPER_MODEL = "whisper-1"


def transcribe_qa_sample(
    audio_bytes: bytes,
    language: str = "en",
    model: str = None,
    response_format: str = "text",
) -> TranscriptResponse:
    client = get_openai_client()

    if model is None:
        model = OPENAI_WHISPER_MODEL

    req = TranscriptRequest(
        audio_bytes=audio_bytes,
        language=language,
        model=model,
        response_format=response_format,
    )

    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = f"qa_sample.{response_format}"

    response = client.audio.transcriptions.create(
        file=audio_file,
        model=model,
        language=language,
        response_format=response_format,
    )

    transcript_text = response.text if hasattr(response, "text") else str(response)

    return TranscriptResponse(
        text=transcript_text.strip(),
        language=language,
        model_used=model,
    )


def verify_synthesis(
    original_text: str, audio_bytes: bytes, language: str = "en", model: str = None
) -> dict:
    transcript = transcribe_qa_sample(audio_bytes, language=language, model=model)

    original_normalized = " ".join(original_text.lower().split())
    transcript_normalized = " ".join(transcript.text.lower().split())

    match_score = _compute_text_similarity(original_normalized, transcript_normalized)

    return {
        "original_text": original_text,
        "transcribed_text": transcript.text,
        "match_score": match_score,
        "language": language,
        "model_used": transcript.model_used,
    }


def _compute_text_similarity(text_a: str, text_b: str) -> float:
    words_a = set(text_a.split())
    words_b = set(text_b.split())

    if not words_a or not words_b:
        return 0.0

    intersection = words_a & words_b
    union = words_a | words_b

    return len(intersection) / len(union)
