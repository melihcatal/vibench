import os
import secrets
import urllib.parse
import webbrowser


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI", "http://localhost:8080/callback")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")
AUTH0_SCOPE = os.environ.get("AUTH0_SCOPE", "openid profile email")


def build_authorization_url() -> str:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        raise RuntimeError("AUTH0_DOMAIN and AUTH0_CLIENT_ID are required")

    state = secrets.token_urlsafe(24)
    nonce = secrets.token_urlsafe(24)
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": AUTH0_SCOPE,
        "state": state,
        "nonce": nonce,
    }
    if AUTH0_AUDIENCE:
        params["audience"] = AUTH0_AUDIENCE

    query = urllib.parse.urlencode(params)
    return f"https://{AUTH0_DOMAIN}/authorize?{query}"


def main() -> None:
    url = build_authorization_url()
    print(url)
    webbrowser.open(url)


if __name__ == "__main__":
    main()
