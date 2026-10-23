import os
import sys
import json
import base64
from urllib import request, parse, error


def refresh_session(refresh_token: str) -> dict:
    token_url = "https://oauth2.googleapis.com/token"
    data = parse.urlencode(
        {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
            "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
    ).encode("utf-8")
    req = request.Request(token_url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    refresh_token = os.environ.get("GOOGLE_REFRESH_TOKEN")
    if not refresh_token and len(sys.argv) > 1:
        refresh_token = sys.argv[1]
    if not refresh_token:
        raise SystemExit(1)
    try:
        result = refresh_session(refresh_token)
    except error.HTTPError as exc:
        sys.stdout.write(exc.read().decode("utf-8"))
        return 1
    sys.stdout.write(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
