from __future__ import annotations

import assemblyai as aai

from speech_client import create_client
from speech_models import normalize_result


def diarized_transcript(audio_file: str) -> dict:
    transcriber = create_client()
    config = aai.TranscriptionConfig(speaker_labels=True, punctuate=True, format_text=True)
    transcript = transcriber.transcribe(audio_file, config=config)
    return normalize_result(transcript).__dict__


if __name__ == "__main__":
    raise SystemExit("import and call diarized_transcript(audio_file)")
