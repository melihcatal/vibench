import boto3


def speech_client():
    client = boto3.client("transcribe")
    return client
