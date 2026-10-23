import base64
import hashlib
import os
import secrets
import urllib.parse


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_REDIRECT_URI_ENV = "AUTH0_REDIRECT_URI"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_SCOPE_ENV = "AUTH0_SCOPE"


def _b64url_no_pad(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _pkce_pair() -> tuple[str, str]:
    verifier = _b64url_no_pad(secrets.token_bytes(32))
    challenge = _b64url_no_pad(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def build_authorization_url(state: str | None = None) -> tuple[str, str, str]:
    domain = os.environ[AUTH0_DOMAIN_ENV].strip()
    client_id = os.environ[AUTH0_CLIENT_ID_ENV].strip()
    redirect_uri = os.environ[AUTH0_REDIRECT_URI_ENV].strip()
    audience = os.getenv(AUTH0_AUDIENCE_ENV, "").strip()
    scope = os.getenv(AUTH0_SCOPE_ENV, "openid profile email").strip()
    if not state:
        state = _b64url_no_pad(secrets.token_bytes(16))
    verifier, challenge = _pkce_pair()

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    if audience:
        params["audience"] = audience

    url = f"https://{domain}/authorize?{urllib.parse.urlencode(params)}"
    return url, verifier, state


def main() -> None:
    url, verifier, state = build_authorization_url()
    print(url)
    print(verifier)
    print(state)


if __name__ == "__main__":
    main()
