import os
import secrets

from identity_client import IdentityClientConfig, build_authorization_url, generate_pkce_challenge
from identity_models import AuthCodeRequest

def start_pkce_login_flow():
    # Generate PKCE code verifier and challenge
    code_verifier, code_challenge = generate_pkce_challenge()

    # Generate a secure state parameter
    state = secrets.token_urlsafe(32)

    # In a real application, you would store the code_verifier and state
    # in the user's session for verification during the callback.
    # For this example, we'll just print them.
    print(f"Generated PKCE Code Verifier: {code_verifier}")
    print(f"Generated State: {state}")

    auth_request = AuthCodeRequest(
        client_id=IdentityClientConfig.AZURE_AD_CLIENT_ID,
        redirect_uri=IdentityClientConfig.REDIRECT_URI,
        scope="openid profile email User.Read",
        response_type="code",
        state=state,
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )

    authorization_url = build_authorization_url(
        client_id=auth_request.client_id,
        redirect_uri=auth_request.redirect_uri,
        scope=auth_request.scope,
        state=auth_request.state,
        response_type=auth_request.response_type,
        code_challenge=auth_request.code_challenge,
        code_challenge_method=auth_request.code_challenge_method
    )

    print(f"Please navigate to the following URL to initiate PKCE login:\n{authorization_url}")
    return authorization_url, code_verifier, state

if __name__ == "__main__":
    # Example usage: Ensure environment variables are set for a real flow
    # os.environ["AZURE_AD_CLIENT_ID"] = "YOUR_AZURE_AD_CLIENT_ID"
    # os.environ["AZURE_AD_TENANT_ID"] = "YOUR_AZURE_AD_TENANT_ID"
    # os.environ["REDIRECT_URI"] = "http://localhost:8000/oauth/callback"
    url, verifier, state = start_pkce_login_flow()
