import os
import json
import urllib.request
import urllib.error


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CONNECTION = os.environ.get("AUTH0_CONNECTION")


def start_password_reset(email: str) -> dict:
    if not AUTH0_DOMAIN:
        raise RuntimeError("AUTH0_DOMAIN is required")
    if not AUTH0_CLIENT_ID:
        raise RuntimeError("AUTH0_CLIENT_ID is required")
    if not AUTH0_CONNECTION:
        raise RuntimeError("AUTH0_CONNECTION is required")

    url = f"https://{AUTH0_DOMAIN}/dbconnections/change_password"
    payload = json.dumps(
        {
            "client_id": AUTH0_CLIENT_ID,
            "email": email,
            "connection": AUTH0_CONNECTION,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return {"ok": True, "response": body}
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8") if exc.fp else ""
        return {"ok": False, "status": exc.code, "error": error_body}


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("usage: password_reset.py <email>")
    result = start_password_reset(sys.argv[1])
    print(json.dumps(result))
