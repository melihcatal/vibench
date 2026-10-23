import boto3

def get_translate_client(region_name='us-west-2'):
    return boto3.client('translate', region_name=region_name)