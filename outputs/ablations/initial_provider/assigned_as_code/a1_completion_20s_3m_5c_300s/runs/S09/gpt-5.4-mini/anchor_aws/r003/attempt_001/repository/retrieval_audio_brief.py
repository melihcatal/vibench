import os

import boto3


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region") or os.environ.get("AWS_REGION", "us-east-1"))
    text = payload["text"]
    response = client.synthesize_speech(OutputFormat="mp3", Text=text, VoiceId=config.get("voice_id", "Joanna"), Engine=config.get("engine", "neural"))
    stream = response["AudioStream"]
    try:
        return {"audio": stream.read()}
    finally:
        stream.close()
