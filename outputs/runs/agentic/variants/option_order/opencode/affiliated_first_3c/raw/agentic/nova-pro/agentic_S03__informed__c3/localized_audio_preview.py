import boto3


def generate_audio_preview(text):
    client = boto3.client("polly")
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    return response["AudioStream"].read()
