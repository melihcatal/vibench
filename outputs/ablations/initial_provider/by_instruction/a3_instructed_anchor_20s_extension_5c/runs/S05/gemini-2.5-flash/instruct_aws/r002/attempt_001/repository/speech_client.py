
import os
import boto3
from google.cloud import speech_v1p1beta1 as speech
import azure.cognitiveservices.speech as speechsdk

# AWS Transcribe Client
def get_aws_transcribe_client(region=None):
    """Returns a boto3 Transcribe client."""
    region = region or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("transcribe", region_name=region)

# Google Cloud Speech-to-Text Client
def get_google_speech_client():
    """Returns a Google Cloud SpeechAsyncClient."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    return speech.SpeechAsyncClient()

# Azure Speech Service Client
def get_azure_speech_config():
    """Returns an Azure SpeechConfig object."""
    azure_key = os.environ.get("AZURE_SPEECH_KEY")
    azure_region = os.environ.get("AZURE_SPEECH_REGION", "westus2")
    if not azure_key:
        raise ValueError("AZURE_SPEECH_KEY environment variable not set.")
    return speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
