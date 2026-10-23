import os

import boto3


def localized_audio_preview(text, voice_id="Joanna", region_name=None):
    polly = boto3.client("polly", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1")
    return polly.synthesize_speech(Text=str(text), OutputFormat="mp3", VoiceId=voice_id)
