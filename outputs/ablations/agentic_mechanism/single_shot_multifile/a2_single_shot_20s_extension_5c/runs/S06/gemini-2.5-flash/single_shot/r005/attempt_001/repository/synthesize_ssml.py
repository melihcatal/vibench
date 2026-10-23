import os
import boto3

def synthesize_ssml(ssml_text: str, voice_id: str = "Joanna", output_format: str = "mp3") -> bytes:
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    polly_client = boto3.client(
        "polly",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    response = polly_client.synthesize_speech(
        Text=ssml_text,
        OutputFormat=output_format,
        VoiceId=voice_id,
        TextType='ssml'
    )

    if "AudioStream" in response:
        return response["AudioStream"].read()
    else:
        raise Exception("Could not get audio stream from AWS Polly")
