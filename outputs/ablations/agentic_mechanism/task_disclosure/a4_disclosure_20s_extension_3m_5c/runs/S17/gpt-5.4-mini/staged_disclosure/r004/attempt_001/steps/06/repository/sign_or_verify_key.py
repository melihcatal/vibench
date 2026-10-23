import base64
import json
import os
import sys
from typing import Any, Dict, Optional

import requests


GOOGLE_KMS_BASE_URL = "https://cloudkms.googleapis.com/v1"


def _access_token() -> str:
    token = os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN") or os.environ.get("GCP_ACCESS_TOKEN")
    if token:
        return token
    try:
        import google.auth
        from google.auth.transport.requests import Request

        credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        if not credentials.valid:
            credentials.refresh(Request())
        if not credentials.token:
            raise RuntimeError("Unable to obtain Google Cloud access token")
        return credentials.token
    except Exception as exc:
        raise RuntimeError("Missing Google Cloud authentication") from exc


def _headers() -> Dict[str, str]:
    return {"Authorization": f"Bearer {_access_token()}", "Content-Type": "application/json"}


def sign_key(resource_name: str, payload: bytes) -> Dict[str, Any]:
    url = f"{GOOGLE_KMS_BASE_URL}/{resource_name}:asymmetricSign"
    body = {"digest": {"sha256": base64.b64encode(payload).decode("ascii")}}
    response = requests.post(url, headers=_headers(), data=json.dumps(body), timeout=30)
    response.raise_for_status()
    return response.json()


def verify_key(resource_name: str, message: bytes, signature: bytes) -> Dict[str, Any]:
    url = f"{GOOGLE_KMS_BASE_URL}/{resource_name}:asymmetricVerify"
    body = {
        "digest": {"sha256": base64.b64encode(message).decode("ascii")},
        "signature": base64.b64encode(signature).decode("ascii"),
    }
    response = requests.post(url, headers=_headers(), data=json.dumps(body), timeout=30)
    response.raise_for_status()
    return response.json()


def _main(argv: Optional[list] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) < 3:
        print("usage: sign_or_verify_key.py <sign|verify> <resource_name> <payload> [signature_b64]", file=sys.stderr)
        return 2
    action, resource_name, payload = args[0], args[1], args[2].encode("utf-8")
    if action == "sign":
        result = sign_key(resource_name, payload)
    elif action == "verify":
        if len(args) < 4:
            print("verify requires signature_b64", file=sys.stderr)
            return 2
        result = verify_key(resource_name, payload, base64.b64decode(args[3]))
    else:
        print("action must be sign or verify", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
