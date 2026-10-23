"""Generate spoken previews of translated copy using Amazon Polly."""

from __future__ import annotations

from typing import Optional

import boto3

POLLY_VOICE_ID = "Joanna"


def generate_audio_preview(text: str, voice_id: Optional[str] = None) -> bytes:
    client = boto3.client("polly")
    response = client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_id or POLLY_VOICE_ID,
        Engine="neural",
    )
    return response["AudioStream"].read()


__all__ = ["generate_audio_preview", "POLLY_VOICE_ID", "boto3"]
