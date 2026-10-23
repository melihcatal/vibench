import boto3

transcribe_client = boto3.client("transcribe", region_name="us-west-2")


def get_speech_client():
    return transcribe_client


def configure_client():
    # Provide local configuration and client helper utilities for Streaming Speech-to-Text
    pass
