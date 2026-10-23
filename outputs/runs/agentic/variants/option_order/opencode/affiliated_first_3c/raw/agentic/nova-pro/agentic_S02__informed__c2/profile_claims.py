import boto3


def profile_claims(access_token):
    client = boto3.client("cognito-idp")
    response = client.get_user(AccessToken=access_token)
    return response
