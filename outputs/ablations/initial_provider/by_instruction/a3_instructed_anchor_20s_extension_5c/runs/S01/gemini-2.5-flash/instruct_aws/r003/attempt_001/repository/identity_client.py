import os
import boto3

class CognitoClient:
    def __init__(self, user_pool_id=None, client_id=None, region_name=None):
        self.user_pool_id = user_pool_id or os.environ.get("COGNITO_USER_POOL_ID")
        self.client_id = client_id or os.environ.get("COGNITO_CLIENT_ID")
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")

        if not self.user_pool_id or not self.client_id:
            raise ValueError("AWS Cognito User Pool ID and Client ID must be provided or set in environment variables.")

        self._client = boto3.client("cognito-idp", region_name=self.region_name)

    def get_client(self):
        return self._client

    def get_user_pool_id(self):
        return self.user_pool_id

    def get_client_id(self):
        return self.client_id
