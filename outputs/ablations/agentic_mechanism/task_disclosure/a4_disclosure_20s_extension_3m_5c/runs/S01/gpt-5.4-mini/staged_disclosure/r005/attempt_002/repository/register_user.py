import json
import os
import sys
from urllib import request, error


def register_user(email: str, password: str) -> dict:
    api_key = os.environ["FIREBASE_WEB_API_KEY"]
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    payload = json.dumps({"email": email, "password": password, "returnSecureToken": True}).encode("utf-8")
    req = request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(body) from exc


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: python register_user.py <email> <password>")
    result = register_user(sys.argv[1], sys.argv[2])
    print(json.dumps(result))
