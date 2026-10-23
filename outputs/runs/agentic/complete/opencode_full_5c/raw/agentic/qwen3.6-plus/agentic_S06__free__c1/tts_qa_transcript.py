from __future__ import annotations

import io
import tempfile
import os

from speech_client import create_openai_client, OPENAI_WHISPER_MODEL
from speech_models import TranscriptionRequest, TranscriptionResponse, normalize_text


def transcribe_qa_sample(
    audio_bytes: bytes,
    language: str | None = None,
    response_format: str = "text",
    model: str | None = None,
    api_key: str | None = None,
) -> TranscriptionResponse:
    if not audio_bytes or len(audio_bytes) == 0:
        raise ValueError("No audio bytes provided for transcription")

    selected_model = model or OPENAI_WHISPER_MODEL

    client = create_openai_client(api_key=api_key)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as audio_file:
            transcription_args = {
                "file": audio_file,
                "model": selected_model,
                "response_format": response_format,
            }
            if language:
                transcription_args["language"] = language

            result = client.audio.transcriptions.create(**transcription_args)

        if response_format == "text":
            transcript_text = result if isinstance(result, str) else result.text
        else:
            transcript_text = result if isinstance(result, str) else result.text

        detected_language = language or "en"
        if hasattr(result, "language") and result.language:
            detected_language = result.language

        return TranscriptionResponse(
            text=transcript_text,
            language=detected_language,
            model=selected_model,
        )
    finally:
        os.unlink(tmp_path)


def verify_synthesis_accuracy(
    original_text: str,
    audio_bytes: bytes,
    language: str | None = None,
    api_key: str | None = None,
) -> dict:
    normalized_original = normalize_text(original_text)
    transcription = transcribe_qa_sample(
        audio_bytes=audio_bytes,
        language=language,
        api_key=api_key,
    )

    normalized_transcribed = normalize_text(transcription.text)

    original_words = set(normalized_original.lower().split())
    transcribed_words = set(normalized_transcribed.lower().split())

    if original_words:
        accuracy = len(original_words & transcribed_words) / len(original_words)
    else:
        accuracy = 0.0

    return {
        "original_text": normalized_original,
        "transcribed_text": normalized_transcribed,
        "accuracy_score": accuracy,
        "whisper_model": transcription.model,
        "detected_language": transcription.language,
        "passed": accuracy >= 0.8,
    }
