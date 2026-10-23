import os
from google.cloud import texttospeech
import boto3

def get_google_tts_client():
    # Google Cloud client setup usually relies on GOOGLE_APPLICATION_CREDENTIALS
    # or default project configuration.
    return texttospeech.TextToSpeechClient()

def get_aws_polly_client():
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set for Polly.")

    return boto3.client(
        "polly",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

def get_azure_tts_config():
    azure_speech_key = os.environ.get("AZURE_SPEECH_KEY")
    azure_speech_region = os.environ.get("AZURE_SPEECH_REGION", "eastus")

    if not azure_speech_key:
        raise ValueError("AZURE_SPEECH_KEY must be set for Azure TTS.")

    return {
        "key": azure_speech_key,
        "region": azure_speech_region
    }
