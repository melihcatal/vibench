import boto3

def get_cognito_client(config=None):
    config = config or {}
    return boto3.client('cognito-idp', region_name=config.get('region'))