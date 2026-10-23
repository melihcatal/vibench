import boto3

def get_transcribe_client(region=None):
    return boto3.client('transcribe', region_name=region or 'us-east-1')

def get_translate_client(region=None):
    return boto3.client('translate', region_name=region or 'us-east-1')

def get_comprehend_client(region=None):
    return boto3.client('comprehend', region_name=region or 'us-east-1')

def get_polly_client(region=None):
    return boto3.client('polly', region_name=region or 'us-east-1')