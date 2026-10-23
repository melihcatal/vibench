import boto3

def get_translate_client():
    return boto3.client('translate', region_name='us-west-2')