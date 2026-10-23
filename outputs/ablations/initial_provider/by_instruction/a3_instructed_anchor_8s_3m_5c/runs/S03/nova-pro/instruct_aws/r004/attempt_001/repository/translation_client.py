import boto3

def get_translate_client():
    return boto3.client('translate')