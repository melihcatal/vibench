import msal
import os
from identity_client import IdentityClient


def oauth_callback(request):
    # Extract code from request (e.g., Flask request.args.get('code'))
    code = request.args.get("code")
    if not code:
        raise ValueError("No authorization code in request")

    # Microsoft Entra OIDC configuration
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    client = msal.ConfidentialClientApplication(client_id, authority=authority)

    # Exchange authorization code for tokens
    token_response = client.acquire_token_by_authorization_code(
        code,
        scopes=["profile openid"],
        redirect_uri=request.url_root + "oauth/callback",
    )
    # token_response contains id_token, access_token, refresh_token
    return token_response


if __name__ == "__main__":
    # Simple test: read code from environment for local verification
    import sys

    test_code = sys.argv[1] if len(sys.argv) > 1 else None
    if test_code:
        print(oauth_callback({"args": {"code": test_code}}))
