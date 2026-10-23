import os
from urllib.parse import urlparse

class CognitoConfig:
    def __init__(self):
        self.region = os.environ.get("COGNITO_REGION", "us-east-1")
        self.user_pool_id = os.environ.get("COGNITO_USER_POOL_ID")
        self.client_id = os.environ.get("COGNITO_CLIENT_ID")
        self.client_secret = os.environ.get("COGNITO_CLIENT_SECRET")
        self.domain_prefix = os.environ.get("COGNITO_DOMAIN_PREFIX")

        if not self.user_pool_id or not self.client_id or not self.domain_prefix:
            raise ValueError("Missing one or more Cognito environment variables: COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID, COGNITO_DOMAIN_PREFIX")

        self.token_endpoint = f"https://{self.domain_prefix}.auth.{self.region}.amazoncognito.com/oauth2/token"
        self.userinfo_endpoint = f"https://{self.domain_prefix}.auth.{self.region}.amazoncognito.com/oauth2/userInfo"


def get_cognito_config():
    return CognitoConfig()
