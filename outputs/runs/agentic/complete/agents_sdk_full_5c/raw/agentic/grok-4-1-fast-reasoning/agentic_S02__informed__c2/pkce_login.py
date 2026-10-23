import msal
from identity_client import get_config, generate_pkce_pair, generate_state

config = get_config()

app = msal.PublicClientApplication(
    config["client_id"],
    authority=config["authority"]
)

def start_pkce_login():
    state = generate_state()
    verifier, challenge = generate_pkce_pair()
    auth_url = app.get_authorization_request_url(
        config["scopes"],
        redirect_uri=config["redirect_uri"],
        state=state,
        code_challenge=challenge,
        code_challenge_method="S256"
    )
    return auth_url, state, verifier

def exchange_pkce_code(code: str, verifier: str, state: str):
    result = app.acquire_token_by_authorization_code(
        code,
        scopes=config["scopes"],
        redirect_uri=config["redirect_uri"],
        code_verifier=verifier
    )
    if "access_token" in result:
        return result
    raise ValueError(result.get("error_description"))

# Provider-specific: msal PublicClientApplication with PKCE explicit