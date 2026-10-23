import boto3

def fetch_and_normalize_profile_claims(user_pool_id, user_name):
    client = boto3.client('cognito-idp')
    response = client.admin_get_user(
        UserPoolId=user_pool_id,
        Username=user_name
    )
    normalized_claims = {}
    for attribute in response['UserAttributes']:
        normalized_claims[attribute['Name']] = attribute['Value']
    return normalized_claims