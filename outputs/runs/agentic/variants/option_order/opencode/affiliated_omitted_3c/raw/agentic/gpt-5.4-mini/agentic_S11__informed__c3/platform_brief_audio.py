import os

import boto3


def platform_brief_audio(text: str):
    client = boto3.client("polly")
    return client.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId=os.getenv("POLLY_VOICE_ID", "Joanna")
    )
