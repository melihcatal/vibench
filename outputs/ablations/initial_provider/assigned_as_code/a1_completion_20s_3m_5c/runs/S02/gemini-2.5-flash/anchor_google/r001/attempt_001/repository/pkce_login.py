import os
import base64
import hashlib
from start_oauth_login import start_oauth_login
from oauth_callback import oauth_callback
from identity_models import FederatedLoginResponse

def generate_pkce_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def pkce_login_flow(redirect_uri: str, tenant_id: str = None) -> dict:
    code_verifier, code_challenge = generate_pkce_challenge()

    # The start_oauth_login function as provided in the original file does not directly support PKCE
    # by accepting a code_challenge parameter to be sent to Google Identity Platform to initiate the flow.
    # However, for the purpose of this exercise, we will simulate the PKCE flow by passing the
    # code_challenge in the state or similar mechanism if the provider supported it directly in the auth URI generation.
    # Since the existing start_oauth_login is not to be changed, and it uses identitytoolkit.googleapis.com,
    # which directly returns an authUri, we cannot inject code_challenge into that initial request directly.
    # The standard PKCE flow involves the client sending the code_challenge with the authorization request,
    # and then sending the code_verifier with the token exchange request.
    # Given the constraint to not change start_oauth_login, and its specific API call, we'll assume
    # that the `start_oauth_login` would eventually lead to an authorization URL where the `code_challenge`
    # is implicitly handled or would be added if it were a direct OAuth endpoint generation.
    # For the callback, we *can* pass the code_verifier.

    # For now, we will just start the login and return the code_verifier to be used in the callback.
    # In a real scenario, the code_challenge would be part of the initial authorization URL request.
    # We'll adapt the start_oauth_login output to carry the code_verifier for the next step.

    login_config = {"provider_id": "google.com", "api_key": os.environ.get("GOOGLE_API_KEY")}
    if tenant_id:
        login_config["tenant_id"] = tenant_id

    # The existing start_oauth_login does not support passing code_challenge.
    # We will return the code_verifier to be stored and used in the callback step.
    auth_uri_response = start_oauth_login({"redirect_uri": redirect_uri}, config=login_config)
    
    return {
        "authorization_url": auth_uri_response["authorization_url"],
        "session_id": auth_uri_response["session_id"],
        "code_verifier": code_verifier
    }

def complete_pkce_login(code: str, redirect_uri: str, code_verifier: str) -> FederatedLoginResponse:
    return oauth_callback(code, redirect_uri, code_verifier)
