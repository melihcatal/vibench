import os
import boto3

class CognitoClient:
    def __init__(self):
        self.cognito_client = boto3.client("cognito-idp", region_name=os.environ.get("AWS_REGION", "us-east-1"))
        self.client_id = os.environ.get("COGNITO_CLIENT_ID")
        self.client_secret = os.environ.get("COGNITO_CLIENT_SECRET")
        self.user_pool_id = os.environ.get("COGNITO_USER_POOL_ID")
        self.redirect_uri = os.environ.get("COGNITO_REDIRECT_URI")
        self.domain_url = os.environ.get("COGNITO_DOMAIN_URL")
