import boto3


def synthesize_ssml(ssml):
    polly_client = boto3.client("polly")
    response = polly_client.synthesize_speech(
        Text=ssml, OutputFormat="mp3", TextType="ssml", VoiceId="Joanna"
    )
    return response["AudioStream"].read()
