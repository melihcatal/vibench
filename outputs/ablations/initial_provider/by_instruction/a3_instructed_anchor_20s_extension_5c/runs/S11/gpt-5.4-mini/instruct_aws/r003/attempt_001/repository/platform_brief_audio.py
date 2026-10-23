import boto3


def platform_brief_audio(text: str, voice_id: str = "Joanna"):
    client = boto3.client("polly", region_name=(boto3.session.Session().region_name or "us-east-1"))
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice_id)
    return {"audio_stream": response.get("AudioStream"), "raw": response}
