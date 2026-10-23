import secrets

from identity_client import microsoft_authorize_url, oauth_request, microsoft_client_id


def build_pkce_login_url(redirect_uri: str) -> str:
    state = secrets.token_urlsafe(24)
    verifier = secrets.token_urlsafe(64)
    request = oauth_request(redirect_uri, state, verifier)
    return (
        f"{microsoft_authorize_url()}?client_id={microsoft_client_id()}"
        f"&response_type=code&redirect_uri={redirect_uri}&response_mode=query"
        f"&scope=openid%20profile%20email%20offline_access"
        f"&state={state}&code_challenge={request.code_challenge}&code_challenge_method=S256"
    )
