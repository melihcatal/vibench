import boto3


def platform_brief_audio(payload, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region", "us-east-1"))
    result = client.synthesize_speech(
        Text=payload["text"],
        OutputFormat=config.get("output_format", "mp3"),
        VoiceId=config.get("voice_id", "Joanna"),
    )
    audio_stream = result.get("AudioStream")
    return {"audio_stream": audio_stream, "voiceId": config.get("voice_id", "Joanna")}
