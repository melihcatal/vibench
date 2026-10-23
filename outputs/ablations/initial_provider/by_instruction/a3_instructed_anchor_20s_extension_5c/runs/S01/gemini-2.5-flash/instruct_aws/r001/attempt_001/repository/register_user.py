import boto3
import os

def register_user(email, password):
    client = boto3.client(
        'cognito-idp',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    user_pool_id = os.environ.get('COGNITO_USER_POOL_ID')
    client_id = os.environ.get('COGNITO_CLIENT_ID')

    try:
        response = client.sign_up(
            ClientId=client_id,
            SecretHash='',  # Not needed if client secret is not enabled for the app client
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ]
        )
        return response
    except client.exceptions.UsernameExistsException:
        raise ValueError("User with this email already exists.")
    except Exception as e:
        raise RuntimeError(f"Cognito registration failed: {e}")
