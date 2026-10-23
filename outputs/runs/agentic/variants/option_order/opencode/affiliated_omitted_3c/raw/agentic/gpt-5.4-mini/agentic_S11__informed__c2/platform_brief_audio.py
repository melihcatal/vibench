import boto3


def platform_brief_audio(text: str):
    client = boto3.client("polly")
    response = client.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId="Joanna", Engine="neural"
    )
    return response["AudioStream"].read()
