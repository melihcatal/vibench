import boto3

def pkce_login(code_verifier):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        AuthFlow='USER_SRP_AUTH',
        AuthParameters={'USERNAME': 'username', 'SRP_A': 'srp-a', 'CODE_VERIFIER': code_verifier},
        ClientId='your-client-id'
    )
    print(response)