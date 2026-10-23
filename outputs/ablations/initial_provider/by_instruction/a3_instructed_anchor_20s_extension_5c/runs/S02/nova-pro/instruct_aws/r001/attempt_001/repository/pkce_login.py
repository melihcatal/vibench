import boto3

def pkce_login(code_verifier, code_challenge):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        AuthFlow='CUSTOM_AUTH',
        AuthParameters={
            'USERNAME': 'user',
            'PASSWORD': code_verifier,
            'CODE_CHALLENGE': code_challenge
        },
        ClientId='your-client-id'
    )
    print(response)