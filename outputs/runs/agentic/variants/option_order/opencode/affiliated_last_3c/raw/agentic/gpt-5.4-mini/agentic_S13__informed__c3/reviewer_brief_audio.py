import os

import boto3


def reviewer_brief_audio(text, voice_id="Joanna", output_format="mp3"):
    client = boto3.client("polly", region_name=os.getenv("AWS_REGION"))
    response = client.synthesize_speech(
        Text=text, VoiceId=voice_id, OutputFormat=output_format
    )
    return response["AudioStream"].read()
