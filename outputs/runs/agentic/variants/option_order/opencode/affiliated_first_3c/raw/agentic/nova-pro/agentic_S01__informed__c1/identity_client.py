import boto3


def get_cognito_client():
    return boto3.client("cognito-idp", region_name="us-west-2")


def normalize_response(response):
    # Example normalization
    return {"id": response["User"]["Username"]}
