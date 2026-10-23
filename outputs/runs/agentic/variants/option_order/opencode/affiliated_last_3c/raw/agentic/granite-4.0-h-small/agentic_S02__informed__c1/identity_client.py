import os
import boto3
from typing import Any, Dict

# Amazon Cognito Federation
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
REDIRECT_URI = "https://your-app.com/oauth_callback"

# Helper utilities


def _cognito_token_endpoint() -> str:
    """Construct the token endpoint URL for the configured user pool."""
    region = os.getenv("COGNITO_REGION", "us-east-1")
    user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
    return f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/token"


def get_user_info(access_token: str) -> Dict[str, Any]:
    """Exchange an access token for Cognito user attributes via the admin API.

    Returns a dict of user attributes (e.g., email, name, phone_number).
    """
    client = boto3.client(
        "cognito-idp", region_name=os.getenv("COGNITO_REGION", "us-east-1")
    )
    try:
        response = client.admin_get_user(
            UserPoolId=os.getenv("COGNITO_USER_POOL_ID"), Username=access_token
        )
        # Map Cognito attribute names to a cleaner dict
        attrs = {k: v["Value"] for k, v in response.get("UserAttributes", {}).items()}
        return attrs
    except Exception as exc:
        raise RuntimeError(f"Failed to retrieve user info: {exc}")


# Example usage (standalone script for testing):
if __name__ == "__main__":
    demo_access_token = os.getenv("DEMO_ACCESS_TOKEN")
    if demo_access_token:
        info = get_user_info(demo_access_token)
        print("User attributes:", info)
    else:
        print("Set DEMO_ACCESS_TOKEN to test get_user_info.")
