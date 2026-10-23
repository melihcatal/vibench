import boto3

def get_cognito_client(config: dict):
    region = config.get("region")
    if not region:
        raise ValueError("AWS region must be provided in config.")
    return boto3.client("cognito-idp", region_name=region)
