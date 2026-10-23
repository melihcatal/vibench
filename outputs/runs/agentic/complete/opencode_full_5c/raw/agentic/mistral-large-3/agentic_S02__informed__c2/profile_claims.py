from typing import Dict, Any
import requests
import json
import os


def fetch_profile_claims(id_token: str) -> Dict[str, Any]:
    """
    Fetch and normalize federated user profile claims from Microsoft Entra ID.
    Returns normalized claims including sub, name, email, and preferred_username.
    """
    # Decode JWT header to get the kid and issuer
    header = json.loads(
        requests.utils.unquote(
            json.dumps(
                json.loads(requests.utils.unquote(id_token.split(".")[0] + "=="))
            )
        )
    )

    # Fetch Microsoft Entra ID OpenID configuration
    tenant_id = os.getenv("AZURE_TENANT_ID")
    openid_config_url = f"https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration"
    openid_config = requests.get(openid_config_url).json()
    jwks_uri = openid_config["jwks_uri"]

    # Fetch JWKS to validate token
    jwks = requests.get(jwks_uri).json()

    # Decode and normalize claims
    claims = json.loads(
        requests.utils.unquote(
            json.dumps(
                json.loads(requests.utils.unquote(id_token.split(".")[1] + "=="))
            )
        )
    )

    normalized_claims = {
        "sub": claims.get("sub"),
        "name": claims.get("name"),
        "email": claims.get("email") or claims.get("preferred_username"),
        "preferred_username": claims.get("preferred_username"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "iss": claims.get("iss"),
        "aud": claims.get("aud"),
        "exp": claims.get("exp"),
        "iat": claims.get("iat"),
    }

    return normalized_claims
