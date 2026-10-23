import boto3

def fetch_and_normalize_profile_claims(access_token):
    client = boto3.client('cognito-idp')
    response = client.get_user(AccessToken=access_token)
    user_attributes = response['UserAttributes']
    normalized_claims = {}
    for attribute in user_attributes:
        normalized_claims[attribute['Name']] = attribute['Value']
    return normalized_claims