import secrets

from identity_client import pkce_challenge, build_authorize_url


def create_pkce_login() -> dict:
    verifier = secrets.token_urlsafe(64)
    challenge = pkce_challenge(verifier)
    return {"verifier": verifier, "authorization_url": build_authorize_url(state=secrets.token_urlsafe(24), code_challenge=challenge, code_challenge_method="S256"), "provider": "AWS Cognito"}
