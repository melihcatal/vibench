import boto3


def get_transcribe_client(region_name):
    return boto3.client("transcribe", region_name=region_name)
