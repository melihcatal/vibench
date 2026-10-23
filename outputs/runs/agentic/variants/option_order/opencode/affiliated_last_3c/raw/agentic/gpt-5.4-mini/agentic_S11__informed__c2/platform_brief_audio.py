import os

import boto3


def platform_brief_audio(text: str, voice_id: str = "Joanna") -> bytes:
    client = boto3.client("polly")
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice_id)
    return response["AudioStream"].read()
