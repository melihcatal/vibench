import boto3
from urllib.parse import urlencode

def oauth_callback(code, config):
    client = boto3.client('cognito-idp', region_name=config['region'])
    response = client.initiate_auth(
        ClientId=config['client_id'],
        AuthParameters={'CODE': code},
        AuthFlow='CODE'
    )
    return response