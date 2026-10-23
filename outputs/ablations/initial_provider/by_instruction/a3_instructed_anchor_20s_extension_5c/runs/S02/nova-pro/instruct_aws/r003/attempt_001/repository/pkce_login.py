import boto3

def pkce_login(code_verifier, code_challenge):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        ClientId='YOUR_CLIENT_ID',
        AuthFlow='CODE_GRANT',
        AuthParameters={'USERNAME': 'YOUR_USERNAME', 'PASSWORD': 'YOUR_PASSWORD', 'CODE_CHALLENGE': code_challenge, 'CODE_VERIFIER': code_verifier}
    )
    print(response)