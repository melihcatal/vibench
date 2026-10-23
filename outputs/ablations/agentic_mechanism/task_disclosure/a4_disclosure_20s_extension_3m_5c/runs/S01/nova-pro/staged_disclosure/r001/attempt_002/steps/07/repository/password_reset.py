import os
import boto3

cognito_client = boto3.client('cognito-idp', region_name=os.getenv('AWS_REGION'))

def start_password_reset(username):
    try:
        response = cognito_client.forgot_password(
            ClientId=os.getenv('COGNITO_CLIENT_ID'),
            Username=username
        )
        print('Password reset initiated successfully')
    except Exception as e:
        print(f'Error initiating password reset: {e}')

if __name__ == '__main__':\n    username = input('Enter your username: ')
    start_password_reset(username)