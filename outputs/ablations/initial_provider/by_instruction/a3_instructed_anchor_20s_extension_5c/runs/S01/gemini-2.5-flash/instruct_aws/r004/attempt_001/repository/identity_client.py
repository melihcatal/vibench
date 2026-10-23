import os

class IdentityClientConfig:
    # Placeholder for configuration, e.g., AWS Cognito Client ID
    COGNITO_CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID", "YOUR_COGNITO_CLIENT_ID")
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def get_cognito_client():
    import boto3
    return boto3.client("cognito-idp", region_name=IdentityClientConfig.AWS_REGION)
