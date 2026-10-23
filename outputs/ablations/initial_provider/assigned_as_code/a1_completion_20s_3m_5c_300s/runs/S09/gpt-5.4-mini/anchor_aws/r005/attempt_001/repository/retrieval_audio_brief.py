import boto3


def retrieval_audio_brief(payload, config=None):
    client = boto3.client("polly", region_name=(config or {}).get("region", "us-east-1"))
    text = payload.get("summary", "")
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=payload.get("voice_id", "Joanna"), Engine=payload.get("engine", "neural"))
    stream = response["AudioStream"]
    try:
        return {"audio_stream": stream.read()}
    finally:
        stream.close()
