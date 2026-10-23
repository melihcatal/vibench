import os
import secrets
import urllib.parse
import webbrowser

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "http://localhost:8000/callback")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
AUTH0_SCOPE = os.getenv("AUTH0_SCOPE", "openid profile email")


def main():
    if not AUTH0_DOMAIN:
        raise SystemExit("AUTH0_DOMAIN is required")
    if not AUTH0_CLIENT_ID:
        raise SystemExit("AUTH0_CLIENT_ID is required")

    state = secrets.token_urlsafe(32)
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": AUTH0_SCOPE,
        "state": state,
    }
    if AUTH0_AUDIENCE:
        params["audience"] = AUTH0_AUDIENCE

    authorization_url = f"https://{AUTH0_DOMAIN}/authorize?{urllib.parse.urlencode(params)}"
    print(authorization_url)
    webbrowser.open(authorization_url)

    requests.get("https://{}/.well-known/openid-configuration".format(AUTH0_DOMAIN), timeout=10)


if __name__ == "__main__":
    main()
