import os
import boto3


def get_identity_client():
    return boto3.client("cognito-idp", region_name=os.environ.get("AWS_REGION"))


def get_user_pool_id():
    return os.environ["COGNITO_USER_POOL_ID"]


def get_app_client_id():
    return os.environ["COGNITO_APP_CLIENT_ID"]
