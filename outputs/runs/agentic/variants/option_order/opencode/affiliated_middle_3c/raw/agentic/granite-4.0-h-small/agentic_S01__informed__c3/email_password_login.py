import boto3

# Amazon Cognito User Pools integration
# Provider identifiable via boto3 client creation

cognito = boto3.client(
    "cognito-idp",
    aws_access_key_id="YOUR_AWS_ACCESS_KEY_ID",
    aws_secret_access_key="YOUR_AWS_SECRET_ACCESS_KEY",
    region_name="us-east-1",
)


def email_password_login(email, password, user_pool_id, client_id):
    """Sign in a user with email and password.

    Args:
        email (str): User's email address.
        password (str): User's password.
        user_pool_id (str): The Cognito User Pool ID.
        client_id (str): App client ID in the user pool.

    Returns:
        dict: Tokens (Access Token, ID Token, Refresh Token) if login succeeds.
    """
    response = cognito.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=client_id,
        AuthFlow="ADMIN_NO_SRP_AUTH",
        AuthParameters={"USERNAME": email, "PASSWORD": password},
    )
    tokens = {
        "Access Token": response["AuthenticationResult"]["AccessToken"],
        "ID Token": response["AuthenticationResult"]["IdToken"],
        "Refresh Token": response["AuthenticationResult"]["RefreshToken"],
    }
    return tokens
