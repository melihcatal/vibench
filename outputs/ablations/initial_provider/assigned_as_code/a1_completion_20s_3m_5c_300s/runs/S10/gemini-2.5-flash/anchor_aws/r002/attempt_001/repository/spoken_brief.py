import boto3

def generate_spoken_brief(payload, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region"))
    response = client.synthesize_speech(
        Text=payload["text"],
        OutputFormat="mp3",
        VoiceId=payload.get("voice_id", "Joanna"),
    )
    # The audio stream is a StreamingBody object
    audio_stream = response["AudioStream"].read()
    return {"audio_content": audio_stream}
