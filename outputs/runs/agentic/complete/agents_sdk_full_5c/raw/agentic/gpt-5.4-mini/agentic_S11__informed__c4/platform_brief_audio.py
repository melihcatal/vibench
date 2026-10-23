from __future__ import annotations

import boto3

from model_models import AudioResult


def platform_brief_audio(text: str, voice_id: str = "Joanna") -> AudioResult:
    client = boto3.client("polly")
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice_id)
    audio = response["AudioStream"].read()
    return AudioResult(audio_bytes=audio, content_type="audio/mpeg", raw=response)
