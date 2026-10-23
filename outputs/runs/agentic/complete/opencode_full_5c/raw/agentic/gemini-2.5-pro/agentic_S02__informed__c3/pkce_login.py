from identity_client import get_identity_client
from auth0.helpers.pkce import generate_code_verifier, calculate_code_challenge
from identity_models import TokenResponse


def generate_pkce_codes():
    code_verifier = generate_code_verifier()
    code_challenge = calculate_code_challenge(code_verifier)
    return {"code_verifier": code_verifier, "code_challenge": code_challenge}


def get_pkce_login_url(code_challenge: str, state: str):
    client = get_identity_client()

    authorize_url = client.auth0.get_authorize_url(
        redirect_uri=client.callback_url,
        audience=f"https://{client.domain}/api/v2/",
        state=state,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return authorize_url


def exchange_pkce_code_for_token(authorization_code: str, code_verifier: str):
    client = get_identity_client()

    token_data = client.auth0.get_token(
        grant_type="authorization_code",
        code=authorization_code,
        redirect_uri=client.callback_url,
        code_verifier=code_verifier,
    )

    return TokenResponse(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        scope=token_data.get("scope"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type"),
    )
