import identity_client

def password_reset(email: str) -> dict:
    """Start a password reset flow for a local Cognito user.
    Returns the Cognito response containing the flow status.
    """
    client = identity_client.IdentityClient()
    response = client.cognito_admin_initiate_auth(
        AuthFlow="REFRESH_TOKEN_AUTH",  # placeholder for password reset flow
        ClientId=client.config['client_id'],
        UserPool=client.config['user_pool_id'],
        AuthParameters={
            "USERNAME": email,
            "PASSWORD": "***"
        }
    )
    # For actual implementation use AdminResetUserPassword
    reset_response = client.cognito_admin_reset_user_password(
        UserPoolId=client.config['user_pool_id'],
        Username=email
    )
    return reset_response
