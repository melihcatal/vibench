import json
import os
from typing import Any, Dict, Optional

import requests


GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


def exchange_authorization_code(
    code: str,
    redirect_uri: str,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
) -> Dict[str, Any]:
    client_id = client_id or os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = client_secret or os.environ.get("GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise ValueError("GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are required")

    response = requests.post(
        GOOGLE_TOKEN_ENDPOINT,
        data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def oauth_callback_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    params = event.get("queryStringParameters") or {}
    code = params.get("code")
    redirect_uri = params.get("redirect_uri") or os.environ.get("GOOGLE_REDIRECT_URI")

    if not code:
        return {"statusCode": 400, "body": json.dumps({"error": "missing_code"})}
    if not redirect_uri:
        return {"statusCode": 400, "body": json.dumps({"error": "missing_redirect_uri"})}

    try:
        tokens = exchange_authorization_code(code=code, redirect_uri=redirect_uri)
        return {"statusCode": 200, "body": json.dumps(tokens)}
    except requests.HTTPError as exc:
        body = exc.response.text if exc.response is not None else str(exc)
        return {"statusCode": 502, "body": json.dumps({"error": "token_exchange_failed", "details": body})}
    except Exception as exc:
        return {"statusCode": 500, "body": json.dumps({"error": "internal_error", "details": str(exc)})}
