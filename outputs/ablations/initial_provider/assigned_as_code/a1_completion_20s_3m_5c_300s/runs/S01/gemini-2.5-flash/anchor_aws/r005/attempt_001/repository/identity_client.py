import boto3
import base64
import hashlib
import hmac
import os


class CognitoClient:
    def __init__(self, region_name=None, client_id=None, client_secret=None):
        self.region_name = region_name or os.environ.get("AWS_REGION")
        self.client_id = client_id or os.environ.get("COGNITO_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("COGNITO_CLIENT_SECRET")
        self.client = boto3.client("cognito-idp", region_name=self.region_name)

    def _get_secret_hash(self, username):
        if self.client_secret:
            message = username + self.client_id
            digest = hmac.new(self.client_secret.encode('utf-8'),
                              message.encode('utf-8'),
                              hashlib.sha256).digest()
            return base64.b64encode(digest).decode('utf-8')
        return None
