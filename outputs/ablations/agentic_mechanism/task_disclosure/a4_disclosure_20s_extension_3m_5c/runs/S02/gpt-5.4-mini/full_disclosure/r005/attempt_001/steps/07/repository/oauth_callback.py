import json
import os
import urllib.error
import urllib.parse
import urllib.request


GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_CLIENT_ID_ENV = "GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET_ENV = "GOOGLE_CLIENT_SECRET"
GOOGLE_REDIRECT_URI_ENV = "GOOGLE_REDIRECT_URI"


def exchange_authorization_code(code: str, code_verifier: str | None = None) -> dict:
    client_id = os.environ.get(GOOGLE_CLIENT_ID_ENV, "")
    client_secret = os.environ.get(GOOGLE_CLIENT_SECRET_ENV, "")
    redirect_uri = os.environ.get(GOOGLE_REDIRECT_URI_ENV, "")
    if not client_id:
        raise ValueError(f"Missing required environment variable: {GOOGLE_CLIENT_ID_ENV}")
    if not client_secret:
        raise ValueError(f"Missing required environment variable: {GOOGLE_CLIENT_SECRET_ENV}")
    if not redirect_uri:
        raise ValueError(f"Missing required environment variable: {GOOGLE_REDIRECT_URI_ENV}")
    if not code:
        raise ValueError("Missing authorization code")

    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    if code_verifier:
        data["code_verifier"] = code_verifier

    request = urllib.request.Request(
        GOOGLE_TOKEN_ENDPOINT,
        data=urllib.parse.urlencode(data).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Google token exchange failed: {exc.code} {details}") from exc

    return json.loads(payload)


def handle_oauth_callback(query_string: str) -> dict:
    params = urllib.parse.parse_qs(query_string, keep_blank_values=True)
    error = params.get("error", [None])[0]
    if error:
        description = params.get("error_description", [""])[0]
        raise RuntimeError(f"OAuth callback error: {error}{': ' + description if description else ''}")

    code = params.get("code", [None])[0]
    if not code:
        raise ValueError("Missing authorization code in callback")

    code_verifier = params.get("code_verifier", [None])[0]
    return exchange_authorization_code(code, code_verifier)


if __name__ == "__main__":
    import sys

    query = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(handle_oauth_callback(query)))
