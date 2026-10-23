import boto3

def get_translation_client():
    return boto3.client('translate')