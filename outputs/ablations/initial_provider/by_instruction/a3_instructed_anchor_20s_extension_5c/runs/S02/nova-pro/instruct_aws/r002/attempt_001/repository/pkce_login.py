import boto3

def pkce_login(code_verifier):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        ClientId='YOUR_CLIENT_ID',
        AuthFlow='CODE_GRANT',
        AuthParameters={'USERNAME': 'YOUR_USERNAME', 'CODE_VERIFIER': code_verifier}
    )
    print(response)

if __name__ == '__main__':
    pkce_login('YOUR_CODE_VERIFIER')