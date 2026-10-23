import os
import boto3

class IdentityClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IdentityClient, cls).__new__(cls)
            
            aws_region = os.environ.get("AWS_REGION")
            if not aws_region:
                raise ValueError("AWS_REGION environment variable not set")
            
            cls._instance.client = boto3.client('cognito-idp', region_name=aws_region)
            
            cls.user_pool_id = os.environ.get("COGNITO_USER_POOL_ID")
            if not cls.user_pool_id:
                raise ValueError("COGNITO_USER_POOL_ID environment variable not set")
            
            cls.client_id = os.environ.get("COGNITO_CLIENT_ID")
            if not cls.client_id:
                raise ValueError("COGNITO_CLIENT_ID environment variable not set")
                
        return cls._instance.client

def get_identity_client():
    return IdentityClient().client

def get_user_pool_id():
    return IdentityClient.user_pool_id

def get_client_id():
    return IdentityClient.client_id
