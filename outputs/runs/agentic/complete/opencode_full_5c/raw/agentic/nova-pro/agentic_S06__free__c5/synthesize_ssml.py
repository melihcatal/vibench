import boto3


def synthesize_ssml(ssml):
    polly = boto3.client("polly")
    response = polly.synthesize_speech(
        Text=ssml, OutputFormat="mp3", VoiceId="Joanna", TextType="ssml"
    )
    return response["AudioStream"].read()
