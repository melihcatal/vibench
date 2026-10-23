import boto3


def reviewer_brief_audio(payload, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region", "us-east-1"))
    response = client.synthesize_speech(Text=payload["text"], OutputFormat="mp3", VoiceId=config.get("voice_id", "Joanna"))
    return {"audio_stream": response["AudioStream"].read()}
