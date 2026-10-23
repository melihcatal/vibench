import boto3

def start_password_reset(username, client_id):
    client = boto3.client('cognito-idp')
    try:
        response = client.forgot_password(
            ClientId=client_id,
            Username=username
        )
        print('Password reset initiated successfully')
        return response
    except Exception as e:
        print(f'Error initiating password reset: {e}')
        return None
