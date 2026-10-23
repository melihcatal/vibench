import os
import boto3


def get_speech_client(config=None):
    config = config or {}
    region = config.get("region") or os.getenv("AWS_REGION")
    return boto3.client("transcribe", region_name=region)