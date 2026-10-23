import boto3


def localized_audio_preview(text, voice_id="Joanna"):
    client = boto3.client("polly", region_name="us-east-1")
    return client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice_id)
