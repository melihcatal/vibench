import boto3


def get_cognito_client():
    return boto3.client("cognito-idp")
