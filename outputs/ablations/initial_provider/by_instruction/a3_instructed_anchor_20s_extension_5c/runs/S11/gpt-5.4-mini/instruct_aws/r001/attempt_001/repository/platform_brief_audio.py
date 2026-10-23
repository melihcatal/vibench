import boto3


def platform_brief_audio(text: str, voice_id: str = "Joanna"):
    client = boto3.client("polly")
    return client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice_id)
