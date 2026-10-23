import os

import boto3


def localized_audio_preview(text: str, voice_id: str = "Joanna"):
    region_name = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    client = boto3.client("polly", region_name=region_name)
    response = client.synthesize_speech(
        Text=text,
        VoiceId=voice_id,
        OutputFormat="mp3",
        Engine="neural",
    )
    return {"provider": "aws.polly", "audio_stream": response.get("AudioStream")}
