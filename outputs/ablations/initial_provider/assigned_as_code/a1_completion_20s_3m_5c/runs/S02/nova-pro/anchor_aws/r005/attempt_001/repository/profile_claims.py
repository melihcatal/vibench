import boto3

def profile_claims(access_token, config):
    client = boto3.client('cognito-idp', region_name=config['region'])
    response = client.get_user(
        AccessToken=access_token
    )
    return response['UserAttributes']