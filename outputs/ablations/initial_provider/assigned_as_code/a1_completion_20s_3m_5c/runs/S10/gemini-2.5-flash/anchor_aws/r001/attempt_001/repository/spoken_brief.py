import boto3


def spoken_brief(payload, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region"))
    text = payload["text"]
    voice_id = payload.get("voice_id", "Joanna")  # Default voice

    response = client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_id
    )
    
    audio_stream = response["AudioStream"]
    # In a real application, you would save this to a file or stream it directly.
    # For this exercise, we will return the raw bytes.
    return {"audio_content": audio_stream.read()}
