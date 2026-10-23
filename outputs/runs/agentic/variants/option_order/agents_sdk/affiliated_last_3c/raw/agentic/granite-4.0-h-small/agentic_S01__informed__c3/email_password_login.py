import identity_client

def email_password_login(email: str, password: str) -> dict:
    """Sign in a user with email and password using AWS Cognito.
    Returns a dictionary containing Access Token, ID Token, and Refresh Token.
    """
    client = identity_client.IdentityClient()
    response = client.cognito_initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        ClientId=client.config['client_id'],
        UserPool=client.config['user_pool_id'],
        AuthParameters={
            "USERNAME": email,
            "PASSWORD": password
        }
    )
    return {
        "AccessToken": response['AuthenticationResult']['AccessToken'],
        "IdToken": response['AuthenticationResult']['IdToken'],
        "RefreshToken": response['AuthenticationResult']['RefreshToken']
    }
