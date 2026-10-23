import os
import sys
import json
import argparse
from urllib import request, error


def refresh_google_session(refresh_token: str, client_id: str, client_secret: str):
    data = (
        f"client_id={request.quote(client_id)}&"
        f"client_secret={request.quote(client_secret)}&"
        f"refresh_token={request.quote(refresh_token)}&"
        "grant_type=refresh_token"
    ).encode("utf-8")

    req = request.Request(
        "https://oauth2.googleapis.com/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Google token refresh failed: {exc.code} {body}") from exc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-token", default=os.getenv("GOOGLE_REFRESH_TOKEN"))
    parser.add_argument("--client-id", default=os.getenv("GOOGLE_CLIENT_ID"))
    parser.add_argument("--client-secret", default=os.getenv("GOOGLE_CLIENT_SECRET"))
    args = parser.parse_args()

    if not args.refresh_token or not args.client_id or not args.client_secret:
        raise SystemExit("Missing GOOGLE_REFRESH_TOKEN, GOOGLE_CLIENT_ID, or GOOGLE_CLIENT_SECRET")

    result = refresh_google_session(args.refresh_token, args.client_id, args.client_secret)
    sys.stdout.write(json.dumps(result))


if __name__ == "__main__":
    main()
