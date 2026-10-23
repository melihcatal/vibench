import boto3

def email_password_login(email, password, config=None):
    config = config or {}
    client = boto3.client('cognito-idp', region_name=config.get('region'))
    response = client.initiate_auth(
        ClientId=config['client_id'],
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={'USERNAME': email, 'PASSWORD': password}
    )
    return {'access_token': response['AuthenticationResult']['AccessToken'],
            'refresh_token': response['AuthenticationResult']['RefreshToken']}
