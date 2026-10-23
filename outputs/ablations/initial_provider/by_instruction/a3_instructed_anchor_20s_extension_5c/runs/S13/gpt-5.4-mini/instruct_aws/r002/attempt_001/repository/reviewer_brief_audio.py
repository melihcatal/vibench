import boto3


def reviewer_brief_audio(text, voice_id="Joanna"):
    client = boto3.client("polly", region_name="us-east-1")
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice_id)
    return {"provider": "aws", "audio_stream": response.get("AudioStream")}
