from __future__ import annotations

import os
from typing import Optional

import assemblyai as aai


DEFAULT_POLLING_INTERVAL_MS = 3000


def get_assemblyai_api_key() -> str:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    return api_key


def configure_assemblyai() -> None:
    aai.settings.api_key = get_assemblyai_api_key()


def build_transcriber() -> aai.Transcriber:
    configure_assemblyai()
    return aai.Transcriber()


def build_transcription_config(
    *,
    speaker_labels: bool = False,
    speakers_expected: Optional[int] = None,
    language_code: Optional[str] = None,
) -> aai.TranscriptionConfig:
    configure_assemblyai()
    kwargs = {
        "speaker_labels": speaker_labels,
    }
    if speakers_expected is not None:
        kwargs["speakers_expected"] = speakers_expected
    if language_code:
        kwargs["language_code"] = language_code
    return aai.TranscriptionConfig(**kwargs)
