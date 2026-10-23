import boto3


def generate_spoken_briefing(output):
    client = boto3.client("polly")
    response = client.synthesize_speech(
        Text=output, OutputFormat="mp3", VoiceId="Joanna"
    )
    return response["AudioStream"].read()
