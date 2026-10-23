import boto3


def localized_audio_preview(payload, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region"))
    response = client.synthesize_speech(
        Text=payload["text"],
        OutputFormat="mp3",
        VoiceId=config.get("voice_id", "Joanna"),
        Engine=config.get("engine", "neural"),
    )
    return {
        "text": payload["text"],
        "audio_stream": response["AudioStream"].read(),
    }
