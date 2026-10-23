import base64
import hashlib
import os
import secrets
import sys
import urllib.parse
import webbrowser


AUTHORITY = os.getenv("GOOGLE_OAUTH_AUTHORITY", "https://accounts.google.com")
AUTHORIZE_PATH = "/o/oauth2/v2/auth"
CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
REDIRECT_URI = os.getenv("GOOGLE_OAUTH_REDIRECT_URI", "http://localhost:8080/callback")
SCOPE = os.getenv("GOOGLE_OAUTH_SCOPE", "openid email profile")


def _code_verifier() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("ascii")


def _code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def build_authorization_url() -> str:
    if not CLIENT_ID:
        raise RuntimeError("GOOGLE_OAUTH_CLIENT_ID is required")
    verifier = _code_verifier()
    challenge = _code_challenge(verifier)
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "state": secrets.token_urlsafe(16),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "access_type": "offline",
        "prompt": "consent",
    }
    url = f"{AUTHORITY}{AUTHORIZE_PATH}?{urllib.parse.urlencode(params)}"
    return url


def main() -> int:
    try:
        url = build_authorization_url()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(url)
    webbrowser.open(url, new=1, autoraise=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
