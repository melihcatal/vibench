import boto3

def start_password_reset(email):
    client = boto3.client('cognito-idp', region_name='us-west-2')
    try:
        response = client.forgot_password(
            ClientId='YOUR_CLIENT_ID',
            Username=email
        )
        print('Password reset initiated for', email)
        return response
    except Exception as e:
        print('Error initiating password reset:', e)
        return None