import io
import httpx
from speech_client import (
    OPENAI_WHISPER_ENDPOINT,
    get_openai_headers,
    create_http_client,
    validate_openai_key,
    DEFAULT_WHISPER_MODEL,
)
from speech_models import TranscriptRequest, TranscriptResponse


def transcribe_qa_sample(
    audio_bytes: bytes,
    language: str = "en",
    model: str = DEFAULT_WHISPER_MODEL,
    response_format: str = "json",
) -> TranscriptResponse:
    if not validate_openai_key():
        raise ValueError("OPENAI_API_KEY is not set or invalid")

    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "qa_sample.mp3"

    headers = {
        "Authorization": f"Bearer {get_openai_headers()['Authorization'].split(' ')[1]}",
    }

    with create_http_client() as client:
        response = client.post(
            OPENAI_WHISPER_ENDPOINT,
            headers=headers,
            files={
                "file": ("qa_sample.mp3", audio_file, "audio/mpeg"),
            },
            data={
                "model": model,
                "language": language,
                "response_format": response_format,
            },
        )
        response.raise_for_status()
        data = response.json()

    transcript_text = data.get("text", "")
    detected_language = data.get("language", language)
    duration = data.get("duration", 0.0)

    words = []
    if response_format == "verbose_json":
        words = data.get("words", [])

    return TranscriptResponse(
        text=transcript_text,
        language_detected=detected_language,
        duration_sec=duration,
        model_used=model,
        words=words,
    )


def transcribe_qa_sample_from_file(
    audio_path: str,
    language: str = "en",
    model: str = DEFAULT_WHISPER_MODEL,
) -> TranscriptResponse:
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    return transcribe_qa_sample(
        audio_bytes=audio_bytes,
        language=language,
        model=model,
    )


def verify_synthesis_accuracy(
    original_text: str,
    audio_bytes: bytes,
    language: str = "en",
    model: str = DEFAULT_WHISPER_MODEL,
    similarity_threshold: float = 0.85,
) -> dict:
    transcript = transcribe_qa_sample(
        audio_bytes=audio_bytes,
        language=language,
        model=model,
    )

    original_normalized = " ".join(original_text.lower().split())
    transcript_normalized = " ".join(transcript.text.lower().split())

    original_words = set(original_normalized.split())
    transcript_words = set(transcript_normalized.split())

    if not original_words:
        accuracy = 1.0
    else:
        matching_words = original_words & transcript_words
        accuracy = len(matching_words) / len(original_words)

    passed = accuracy >= similarity_threshold

    return {
        "passed": passed,
        "accuracy": accuracy,
        "original_text": original_text,
        "transcribed_text": transcript.text,
        "language_detected": transcript.language_detected,
        "duration_sec": transcript.duration_sec,
        "model_used": transcript.model_used,
    }
