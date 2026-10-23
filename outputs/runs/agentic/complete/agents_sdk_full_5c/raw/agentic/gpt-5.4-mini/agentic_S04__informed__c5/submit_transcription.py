from __future__ import annotations

from speech_client import create_client, normalize_audio_source
from speech_models import TranscriptionRequest, normalize_result


def submit_transcription(audio_file: str) -> dict:
    config = TranscriptionRequest(audio_source=audio_file)
    transcriber = create_client()
    transcript = transcriber.transcribe(
        normalize_audio_source(config.audio_source),
        config=aai.TranscriptionConfig(
            language_code=config.language_code,
            speaker_labels=config.speaker_labels,
            punctuate=config.punctuate,
            format_text=config.format_text,
            word_boost=config.word_boost,
        ),
    )
    return normalize_result(transcript).__dict__


if __name__ == "__main__":
    raise SystemExit("import and call submit_transcription(audio_file)")
