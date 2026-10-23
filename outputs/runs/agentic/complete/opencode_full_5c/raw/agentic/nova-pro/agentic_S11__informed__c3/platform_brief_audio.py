import boto3

AWS_REGION = "us-west-2"

polly_client = boto3.client("polly", region_name=AWS_REGION)


def generate_briefing(text):
    response = polly_client.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId="Joanna"
    )
    return response["AudioStream"].read()
