import boto3

transcribe = boto3.client("transcribe", region_name="us-west-2")


def get_transcription_client():
    return transcribe
