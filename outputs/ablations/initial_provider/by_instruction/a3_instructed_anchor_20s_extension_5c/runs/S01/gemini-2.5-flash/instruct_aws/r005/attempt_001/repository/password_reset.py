import os
import boto3

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
            SecretHash="string" # This is usually generated on the client-side
        )
        return response
    except client.exceptions.UserNotFoundException:
        return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}
