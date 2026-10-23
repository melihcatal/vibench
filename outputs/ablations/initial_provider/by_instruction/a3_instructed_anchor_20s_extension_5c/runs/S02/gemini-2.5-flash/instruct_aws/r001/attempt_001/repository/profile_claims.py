import os
import boto3

def fetch_profile_claims(access_token: str) -> dict:
    """
    Fetches and normalizes federated user profile claims using AWS Cognito.
    """
    cognito_region = os.environ.get("AWS_REGION")

    if not cognito_region:
        raise ValueError("Missing required environment variable: AWS_REGION")

    client = boto3.client('cognito-idp', region_name=cognito_region)

    try:
        user_info = client.get_user(
            AccessToken=access_token
        )

        # Normalize claims
        normalized_claims = {
            "username": user_info.get("Username"),
            "attributes": {},
            "provider": "AWS_Cognito"
        }

        for attr in user_info.get("UserAttributes", []):
            normalized_claims["attributes"][attr["Name"]] = attr["Value"]

        return normalized_claims
    except client.exceptions.UserNotFoundException:
        return {"error": "User not found or invalid access token."}
    except Exception as e:
        return {"error": str(e)}
