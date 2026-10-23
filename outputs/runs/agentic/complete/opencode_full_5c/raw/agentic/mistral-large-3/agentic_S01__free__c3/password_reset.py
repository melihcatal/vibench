import requests
from typing import Dict, Any
import os


def password_reset(email: str) -> Dict[str, Any]:
    """
    Starts a password reset flow for a local account using AWS Cognito.

    Args:
        email: User email address for password reset

    Returns:
        Dictionary containing password reset initiation response
    """
    cognito_client_id = os.getenv("AWS_COGNITO_CLIENT_ID")
    cognito_region = os.getenv("AWS_COGNITO_REGION")

    cognito_url = f"https://cognito-idp.{cognito_region}.amazonaws.com/"

    payload = {
        "ClientId": cognito_client_id,
        "Username": email,
        "ClientMetadata": {"email": email},
    }

    headers = {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": "AWSCognitoIdentityProviderService.ForgotPassword",
    }

    response = requests.post(cognito_url, json=payload, headers=headers)
    response.raise_for_status()

    return {
        "delivery_details": response.json().get("CodeDeliveryDetails"),
        "provider": "aws_cognito",
        "status": "password_reset_initiated",
    }
