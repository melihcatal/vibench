import boto3


def generate_localized_audio_preview(text, voice_id="Joanna"):
    client = boto3.client("polly")
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice_id)
    return response["AudioStream"].read()
