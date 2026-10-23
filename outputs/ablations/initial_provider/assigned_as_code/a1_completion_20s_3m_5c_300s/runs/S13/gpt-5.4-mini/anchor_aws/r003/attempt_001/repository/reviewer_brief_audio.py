import boto3


def reviewer_brief_audio(payload, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region", "us-east-1"))
    text = payload.get("text", "") if isinstance(payload, dict) else str(payload)
    response = client.synthesize_speech(OutputFormat="mp3", Text=text, VoiceId=config.get("voice_id", "Joanna"))
    return {"audio_stream": response.get("AudioStream")}
