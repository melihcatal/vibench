from __future__ import annotations

import boto3

from safety_models import TTSRequest


POLLY_VOICE_ID = "Joanna"


def generate_reviewer_brief_audio(text: str, voice: str = POLLY_VOICE_ID) -> bytes:
    req = TTSRequest(text=text, voice=voice)
    client = boto3.client("polly")
    response = client.synthesize_speech(Text=req.text, VoiceId=req.voice or POLLY_VOICE_ID, OutputFormat="mp3", Engine="neural")
    return response["AudioStream"].read()
