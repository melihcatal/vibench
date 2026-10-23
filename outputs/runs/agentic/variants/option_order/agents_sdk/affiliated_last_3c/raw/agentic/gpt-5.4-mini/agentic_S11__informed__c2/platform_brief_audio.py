from __future__ import annotations

import os
from typing import Any

import boto3


AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
POLLY_VOICE_ID = os.environ.get("AWS_POLLY_VOICE_ID", "Joanna")


def generate_platform_brief_audio(text: str) -> dict[str, Any]:
    client = boto3.client("polly", region_name=AWS_REGION)
    response = client.synthesize_speech(OutputFormat="mp3", Text=text, VoiceId=POLLY_VOICE_ID)
    return {"audio_stream": response.get("AudioStream"), "content_type": response.get("ContentType"), "request_characters": response.get("RequestCharacters")}
