import os
import boto3

class CognitoIdentityClient:
    def __init__(self):
        self.region_name = os.getenv('AWS_REGION', 'us-east-1')
        self.user_pool_id = os.getenv('COGNITO_USER_POOL_ID')
        self.app_client_id = os.getenv('COGNITO_APP_CLIENT_ID')
        self.client = boto3.client('cognito-idp', region_name=self.region_name)