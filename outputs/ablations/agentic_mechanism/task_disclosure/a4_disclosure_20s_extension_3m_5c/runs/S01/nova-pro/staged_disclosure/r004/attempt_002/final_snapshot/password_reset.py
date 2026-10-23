import boto3

def start_password_reset(username):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': 'placeholder'
        },
        ClientId='your_client_id'
    )
    if 'ChallengeName' in response and response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
        print('Password reset required')
    else:
        print('Password reset not required')

if __name__ == '__main__':
    start_password_reset('user@example.com')