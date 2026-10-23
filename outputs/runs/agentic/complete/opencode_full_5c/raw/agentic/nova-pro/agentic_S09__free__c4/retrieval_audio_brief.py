import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


def generate_spoken_brief(text):
    polly = boto3.client("polly")
    try:
        response = polly.synthesize_speech(
            Text=text, OutputFormat="mp3", VoiceId="Joanna"
        )
        with open("brief.mp3", "wb") as file:
            file.write(response["AudioStream"].read())
    except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
        print(f"Error: {e}")
