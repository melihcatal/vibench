import boto3

def start_password_reset(username):
    client = boto3.client('cognito-idp', region_name='us-west-2')
    try:
        response = client.initiate_auth(
            ClientId='YOUR_COGNITO_CLIENT_ID',
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={'USERNAME': username, 'PASSWORD': 'temp_password'}
        )
        print('Password reset initiated successfully:', response)
    except Exception as e:
        print('Error initiating password reset:', e)

if __name__ == '__main__':
    start_password_reset('example_username')