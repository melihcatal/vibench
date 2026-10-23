import boto3


def localized_audio_preview(payload, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region"))
    response = client.synthesize_speech(
        Text=payload.get("text", ""),
        OutputFormat="mp3",
        VoiceId=config.get("voice_id", "Joanna"),
        Engine=config.get("engine", "neural"),
    )
    return {"audio_stream": response.get("AudioStream")}
