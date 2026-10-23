import os
import boto3

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
            SecretHash="string",  # This is usually generated on the client-side
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ],
        )
        return response
    except client.exceptions.UsernameExistsException:
        return {"error": "Username already exists"}
    except Exception as e:
        return {"error": str(e)}
