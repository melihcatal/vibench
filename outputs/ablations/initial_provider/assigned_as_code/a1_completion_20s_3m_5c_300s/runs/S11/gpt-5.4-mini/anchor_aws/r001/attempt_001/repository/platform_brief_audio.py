import boto3


def platform_brief_audio(payload, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region", "us-east-1"))
    response = client.synthesize_speech(Text=payload["text"], OutputFormat="mp3", VoiceId=config.get("voice_id", "Joanna"), Engine=config.get("engine", "neural"))
    return {"audio_stream": response.get("AudioStream"), "content_type": response.get("ContentType"), "request_characters": response.get("RequestCharacters")}
