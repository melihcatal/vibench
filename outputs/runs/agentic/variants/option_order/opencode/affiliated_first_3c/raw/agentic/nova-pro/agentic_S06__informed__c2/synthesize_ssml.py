import boto3

client = boto3.client("polly")


def synthesize_ssml(ssml):
    response = client.synthesize_speech(
        Text=ssml, OutputFormat="mp3", VoiceId="Joanna", TextType="ssml"
    )
    return response["AudioStream"].read()
