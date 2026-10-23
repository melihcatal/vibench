import boto3

from amazon_transcribe.client import TranscribeStreamingClient

def get_transcribe_client(region=None):
    region = region or boto3.Session().region_name or "us-east-1"
    return TranscribeStreamingClient(region=region)
