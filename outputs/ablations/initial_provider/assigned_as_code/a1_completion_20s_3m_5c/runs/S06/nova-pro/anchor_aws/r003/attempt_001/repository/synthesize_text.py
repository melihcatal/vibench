import boto3


def synthesize_text(payload, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region"))
    response = client.synthesize_speech(Text=payload["text"], TextType="text", OutputFormat="mp3",
                                       VoiceId=config.get("voice_id", "Joanna"))
    stream = response["AudioStream"]
    try:
        return {"audio_bytes": stream.read(), "content_type": "audio/mpeg"}
    finally:
        stream.close()
