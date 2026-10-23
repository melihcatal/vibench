import boto3


def retrieval_audio_brief(text, voice_id, config=None):
    client = boto3.client("polly", region_name=config.get("region", "us-east-1"))
    response = client.synthesize_speech(Text=text, VoiceId=voice_id, OutputFormat="mp3")
    return {"audio_brief": response["AudioStream"].read()}