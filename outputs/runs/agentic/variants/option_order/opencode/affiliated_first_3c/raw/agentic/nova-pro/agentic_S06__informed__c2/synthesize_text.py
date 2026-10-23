import boto3

client = boto3.client("polly")


def synthesize_text(text):
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    return response["AudioStream"].read()
