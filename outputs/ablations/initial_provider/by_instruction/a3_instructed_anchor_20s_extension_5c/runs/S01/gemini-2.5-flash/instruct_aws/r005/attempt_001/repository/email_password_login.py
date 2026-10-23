import os
import boto3

def email_password_login(email, password):
    client = boto3.client(
        'cognito-idp',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    
    client_id = os.environ.get('COGNITO_CLIENT_ID')

    try:
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
                'SECRET_HASH': 'string'  # This is usually generated on the client-side
            }
        )
        return response
    except client.exceptions.NotAuthorizedException:
        return {"error": "Incorrect username or password"}
    except Exception as e:
        return {"error": str(e)}
