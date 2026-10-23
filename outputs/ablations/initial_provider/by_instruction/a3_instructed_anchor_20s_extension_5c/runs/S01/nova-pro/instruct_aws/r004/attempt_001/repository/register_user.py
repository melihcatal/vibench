import boto3

def register_user(username, password, email):
    client = boto3.client('cognito-idp')
    response = client.sign_up(
        ClientId='YOUR_COGNITO_CLIENT_ID',
        Username=username,
        Password=password,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': email
            }
        ]
    )
    return response