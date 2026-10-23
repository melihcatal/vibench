"""Generate spoken briefings from platform outputs using Amazon Polly.

Provider: Amazon Polly via boto3.
Environment: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY.
"""

from __future__ import annotations

import boto3

from model_models import AudioBrief


def generate_platform_brief_audio(text: str) -> AudioBrief:
    client = boto3.client("polly")
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna", Engine="neural")
    audio = response["AudioStream"].read()
    return AudioBrief(text=text, audio_bytes=audio, content_type="audio/mpeg")
