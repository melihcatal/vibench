import boto3


def localized_audio_preview(payload, config=None):
    client = boto3.client("polly", region_name=(config or {}).get("region"))
    response = client.synthesize_speech(
        Text=payload.get("text", ""),
        OutputFormat=payload.get("format", "mp3"),
        VoiceId=payload.get("voice_id", "Joanna"),
        Engine=payload.get("engine", "neural"),
    )
    stream = response.get("AudioStream")
    return {
        "audio": stream.read() if hasattr(stream, "read") else stream,
        "format": payload.get("format", "mp3"),
        "voice_id": payload.get("voice_id", "Joanna"),
    }
