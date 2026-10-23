import boto3

def get_sns_client():
    # AWS SDK import
    return boto3.client('sns')
