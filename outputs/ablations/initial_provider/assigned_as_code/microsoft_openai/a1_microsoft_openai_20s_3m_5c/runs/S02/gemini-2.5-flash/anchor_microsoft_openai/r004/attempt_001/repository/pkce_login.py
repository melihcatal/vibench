import os
import secrets
from identity_client import IdentityClient, generate_pkce_challenge
from identity_models import PkceCodeVerifier


def start_pkce_login_flow(scopes: list, redirect_uri: str):
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    
    if not client_id:
        raise ValueError("Google client ID must be set as an environment variable.")

    # For PKCE, client_secret is not strictly required for public clients, 
    # but IdentityClient expects it. Provide a dummy or empty string.
    identity_client = IdentityClient(client_id, "", redirect_uri)

    pkce_challenge = generate_pkce_challenge()
    code_verifier_obj = PkceCodeVerifier(**pkce_challenge)
    
    state = secrets.token_urlsafe(32)
    authorization_url = identity_client.get_authorization_url(
        scopes, state, code_challenge=code_verifier_obj.code_challenge
    )
    return {
        'authorization_url': authorization_url,
        'session_id': state, # This state should be stored in session for verification later
        'code_verifier': code_verifier_obj.code_verifier # This should be stored in session too
    }
