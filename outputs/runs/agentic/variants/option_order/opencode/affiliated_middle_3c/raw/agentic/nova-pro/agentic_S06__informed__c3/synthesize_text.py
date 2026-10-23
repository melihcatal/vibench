import boto3

polly_client = boto3.client(
    "polly",
    aws_access_key_id="YOUR_AWS_ACCESS_KEY_ID",
    aws_secret_access_key="YOUR_AWS_SECRET_ACCESS_KEY",
    region_name="us-west-2",
)


def synthesize_text(text):
    response = polly_client.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId="Joanna"
    )
    return response["AudioStream"].read()
