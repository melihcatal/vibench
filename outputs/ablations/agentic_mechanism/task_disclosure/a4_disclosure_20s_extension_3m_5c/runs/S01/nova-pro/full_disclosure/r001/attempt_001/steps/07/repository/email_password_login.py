import boto3
from botocore.exceptions import ClientError

def email_password_login(email, password, user_pool_id, client_id):
    client = boto3.client('cognito-idp')
    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={'USERNAME': email, 'PASSWORD': password},
            ClientId=client_id
        )
        return response['AuthenticationResult']
    except ClientError as e:
        print(e)
        return None