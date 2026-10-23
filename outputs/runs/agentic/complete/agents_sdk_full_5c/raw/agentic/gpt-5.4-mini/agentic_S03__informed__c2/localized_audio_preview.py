from __future__ import annotations

import os
from typing import Dict

import boto3

from translation_models import AudioPreviewResult


def localized_audio_preview(text: str, voice_id: str = "Joanna", language_code: str = "en-US") -> AudioPreviewResult:
    client = boto3.client("polly", region_name=os.environ.get("AWS_REGION"))
    response = client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_id,
        LanguageCode=language_code,
    )
    audio_bytes = response["AudioStream"].read()
    return AudioPreviewResult(
        audio_bytes=audio_bytes,
        provider="amazon-polly",
        voice=voice_id,
        content_type="audio/mpeg",
        metadata={"language_code": language_code},
    )
