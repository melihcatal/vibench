from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any

from speech_client import build_transcriber, build_transcription_config, load_config
from speech_models import normalize_segments


def diarized_transcript(audio_file: str) -> List[Dict[str, Any]]:
    cfg = load_config()
    transcriber = build_transcriber(cfg)
    result = transcriber.transcribe(Path(audio_file).as_posix(), config=build_transcription_config(speaker_labels=True))
    return normalize_segments(result)
