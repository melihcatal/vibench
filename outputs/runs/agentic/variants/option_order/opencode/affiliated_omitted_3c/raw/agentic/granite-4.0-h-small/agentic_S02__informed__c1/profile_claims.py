import os
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Cognito Hosted UI Federation
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

client = boto3.client("cognito-idp", region_name=AWS_REGION)


def fetch_user_profile(access_token):
    """Use the Cognito AdminGetUser API to retrieve normalized user attributes.
    Args:
        access_token (str): JWT issued to the client after successful login.
    Returns:
        dict: Normalized user profile with standard claims (email, name, etc.).
    """
    try:
        response = client.admin_get_user(
            UserPoolId=COGNITO_USER_POOL_ID, AccessToken=access_token
        )
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to fetch user profile: {e}")
    # Transform Cognito response into a tidy dict
    profile = {
        "sub": response.get("Username"),
        "email": response.get("UserAttributes", []),
        "name": response.get("UserAttributes", []),
        "given_name": response.get("UserAttributes", []),
        "family_name": response.get("UserAttributes", []),
        # Add additional mapping as needed
    }
    return profile


# Example usage:
# profile = fetch_user_profile(id_token_from_oauth_callback)
# print(profile)
