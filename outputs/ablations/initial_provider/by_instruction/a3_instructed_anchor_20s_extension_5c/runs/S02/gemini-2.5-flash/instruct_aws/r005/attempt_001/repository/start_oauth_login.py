import os
from urllib.parse import urlencode
from identity_client import CognitoClient

def start_oauth_login(scope: str = "openid profile email") -> str:
    cognito_client = CognitoClient()
    if not cognito_client.domain_url or not cognito_client.client_id or not cognito_client.redirect_uri:
        raise ValueError("Missing Cognito configuration environment variables.")

    query_params = {
        "client_id": cognito_client.client_id,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": cognito_client.redirect_uri,
    }
    return f"{cognito_client.domain_url}/oauth2/authorize?{urlencode(query_params)}"
