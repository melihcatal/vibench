import boto3

def register_user(email, password):
    client = boto3.client('cognito-idp', region_name='us-west-2')
    response = client.sign_up(
        ClientId='YOUR_COGNITO_CLIENT_ID',
        Username=email,
        Password=password,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': email
            }
        ]
    )
    return response