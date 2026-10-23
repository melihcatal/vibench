import boto3
import os

def password_reset(email):
    client = boto3.client(
        'cognito-idp',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    client_id = os.environ.get('COGNITO_CLIENT_ID')

    try:
        response = client.forgot_password(
            ClientId=client_id,
            Username=email,
        )
        return response
    except client.exceptions.UserNotFoundException:
        raise ValueError("User with this email not found.")
    except Exception as e:
        raise RuntimeError(f"Cognito password reset initiation failed: {e}")
