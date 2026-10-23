from __future__ import annotations

import os

import assemblyai as aai

from speech_models import BatchTranscriptionRequest


def get_assemblyai_api_key() -> str:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ASSEMBLYAI_API_KEY")
    return api_key


def get_transcriber() -> aai.Transcriber:
    aai.settings.api_key = get_assemblyai_api_key()
    return aai.Transcriber()


def build_transcription_config(
    request: BatchTranscriptionRequest,
) -> aai.TranscriptionConfig:
    return aai.TranscriptionConfig(
        language_code=request.language_code,
        speaker_labels=request.speaker_labels,
        punctuate=request.punctuate,
        format_text=request.format_text,
    )


def get_transcript_base_url() -> str:
    return "https://api.assemblyai.com/v2/transcript"
