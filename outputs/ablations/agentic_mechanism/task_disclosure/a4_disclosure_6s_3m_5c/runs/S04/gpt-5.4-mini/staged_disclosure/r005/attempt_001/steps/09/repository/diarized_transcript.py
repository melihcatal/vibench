import os
from pathlib import Path

from assemblyai import Transcriber, TranscriptionConfig


def diarize_transcript(audio_path: str) -> str:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")

    path = Path(audio_path)
    if not path.is_file():
        raise FileNotFoundError(audio_path)

    transcriber = Transcriber(api_key=api_key)
    config = TranscriptionConfig(speaker_labels=True)
    transcript = transcriber.transcribe(str(path), config=config)

    if transcript.status == "error":
        raise RuntimeError(transcript.error)

    lines = []
    for utterance in transcript.utterances or []:
        lines.append(f"Speaker {utterance.speaker}: {utterance.text}")

    if lines:
        return "\n".join(lines)

    return transcript.text or ""
