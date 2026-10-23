import os
import boto3

# It's recommended to configure region through environment variables
# or a shared configuration file.
AWS_REGION = os.environ.get("AWS_REGION")
COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")
COGNITO_CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")

def get_cognito_client():
    """Initializes and returns a Boto3 Cognito Identity Provider client."""
    if not AWS_REGION:
        raise ValueError("AWS_REGION environment variable is not set.")
    
    return boto3.client("cognito-idp", region_name=AWS_REGION)
