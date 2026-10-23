import boto3

def pkce_login(code_verifier, code_challenge):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        ClientId='YOUR_CLIENT_ID',
        AuthFlow='CUSTOM_AUTH',
        AuthParameters={'USERNAME': 'YOUR_USERNAME', 'ANSWER': code_verifier, 'CODE_CHALLENGE': code_challenge}
    )
    print(response)