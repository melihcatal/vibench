import base64
import hashlib
import os
import secrets
import sys
import urllib.parse
import webbrowser


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def main() -> int:
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    if not client_id:
        print("AUTH0_CLIENT_ID is required", file=sys.stderr)
        return 1

    domain = os.environ.get("AUTH0_DOMAIN")
    if not domain:
        print("AUTH0_DOMAIN is required", file=sys.stderr)
        return 1

    redirect_uri = os.environ.get("AUTH0_REDIRECT_URI", "http://127.0.0.1:8765/callback")
    scope = os.environ.get("AUTH0_SCOPE", "openid profile email")
    state = secrets.token_urlsafe(32)
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())

    auth_url = "https://{}/authorize?{}".format(
        domain,
        urllib.parse.urlencode(
            {
                "response_type": "code",
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "scope": scope,
                "state": state,
                "code_challenge": challenge,
                "code_challenge_method": "S256",
            }
        ),
    )

    print(auth_url)
    if os.environ.get("AUTH0_OPEN_BROWSER", "1") != "0":
        webbrowser.open(auth_url)

    print(state)
    print(verifier)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
