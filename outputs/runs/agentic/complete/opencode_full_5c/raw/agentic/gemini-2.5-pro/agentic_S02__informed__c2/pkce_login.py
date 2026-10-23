import os
import secrets
import hashlib
import base64
from auth0.authentication import GetToken, AuthorizeClient


def generate_pkce_challenge():
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")
    )
    return code_verifier, code_challenge


def get_pkce_login_url(state: str, redirect_uri: str, code_challenge: str) -> str:
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    auth_client = AuthorizeClient(client_id=client_id, domain=domain)

    auth_url = auth_client.get_authorize_url(
        redirect_uri=redirect_uri,
        audience=f"https://{domain}/api/v2/",
        scope="openid profile email",
        response_type="code",
        state=state,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return auth_url


def exchange_pkce_code_for_tokens(
    code: str, redirect_uri: str, code_verifier: str
) -> dict:
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    # Public clients don't use a secret, so we pass None
    get_token = GetToken(domain, client_id, client_secret=None)

    token_info = get_token.authorization_code(
        code, redirect_uri, code_verifier=code_verifier
    )

    return token_info


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    verifier, challenge = generate_pkce_challenge()
    print(f"Code Verifier: {verifier}")
    print(f"Code Challenge: {challenge}")
    print(
        f"PKCE Login URL: {get_pkce_login_url('some_pkce_state', 'http://localhost:3000/callback', challenge)}"
    )
