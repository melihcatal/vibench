import identity_client

def register_user(email: str, password: str) -> dict:
    """Create a new email/password user account via AWS Cognito.
    Returns the response payload from Cognito (includes user confirmation status).
    """
    # Use the helper client configured with AWS credentials
    client = identity_client.IdentityClient()
    # The Cognito AdminCreateUser API requires a user pool ID and client ID
    pool_id = client.config['user_pool_id']
    client_id = client.config['client_id']
    # Call the SDK method
    response = client.cognito_admin_create_user(
        UserPoolId=pool_id,
        Username=email,
        DesiredDeliveryMediums=["EMAIL"],
        UserAttributes=[{"Name": "email", "Value": email}],
        TemporaryPassword=password
    )
    return response
