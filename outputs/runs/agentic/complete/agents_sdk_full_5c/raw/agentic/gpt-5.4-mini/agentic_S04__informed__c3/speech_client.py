from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import assemblyai as aai

DEFAULT_MODEL = "assemblyai/universal-1"


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    language_code: Optional[str] = None
    auto_chapters: bool = False


def load_config() -> SpeechClientConfig:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY", "")
    if not api_key:
        raise EnvironmentError("ASSEMBLYAI_API_KEY is required")
    language_code = os.environ.get("ASSEMBLYAI_LANGUAGE_CODE")
    auto_chapters = os.environ.get("ASSEMBLYAI_AUTO_CHAPTERS", "false").lower() in {"1", "true", "yes"}
    return SpeechClientConfig(api_key=api_key, language_code=language_code, auto_chapters=auto_chapters)


def build_transcriber(config: Optional[SpeechClientConfig] = None) -> aai.Transcriber:
    cfg = config or load_config()
    aai.settings.api_key = cfg.api_key
    return aai.Transcriber(config=aai.TranscriptionConfig(language_code=cfg.language_code, auto_chapters=cfg.auto_chapters))


def build_transcription_config(*, speaker_labels: bool = False, timestamps: bool = False) -> aai.TranscriptionConfig:
    cfg = load_config()
    return aai.TranscriptionConfig(
        language_code=cfg.language_code,
        auto_chapters=cfg.auto_chapters,
        speaker_labels=speaker_labels,
        punctuate=True,
        format_text=True,
        disfluencies=False,
        word_boost=[],
        auto_highlights=False,
        dual_channel=False,
        speaker_labels_expected=None,
        word_timestamps=timestamps,
    )
