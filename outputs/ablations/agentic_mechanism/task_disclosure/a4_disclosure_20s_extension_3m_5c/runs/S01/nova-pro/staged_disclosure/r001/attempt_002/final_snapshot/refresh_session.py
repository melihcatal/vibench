import boto3

def refresh_session():
    client = boto3.client('cognito-idp', region_name='us-east-1')
    try:
        response = client.initiate_auth(
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={'REFRESH_TOKEN': 'your-refresh-token'}
        )
        access_token = response['AuthenticationResult']['AccessToken']
        print(f'New access token: {access_token}')
    except client.exceptions.NotAuthorizedException:
        print('Invalid refresh token.')

if __name__ == '__main__':
    refresh_session()