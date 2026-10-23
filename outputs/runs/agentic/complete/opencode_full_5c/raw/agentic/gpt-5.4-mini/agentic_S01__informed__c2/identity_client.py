import os
from typing import Any, Dict, Optional

import requests

from identity_models import normalize_email, normalize_locale, pick_dict


def auth0_domain() -> str:
    return os.environ["AUTH0_DOMAIN"]


def auth0_client_id() -> str:
    return os.environ.get("AUTH0_CLIENT_ID", "")


def auth0_client_secret() -> str:
    return os.environ.get("AUTH0_CLIENT_SECRET", "")


def auth0_audience() -> str:
    return os.environ.get("AUTH0_AUDIENCE", f"https://{auth0_domain()}/api/v2/")


def auth0_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def auth0_request(
    method: str, path: str, token: Optional[str] = None, **kwargs: Any
) -> requests.Response:
    headers = dict(auth0_headers())
    if token:
        headers["Authorization"] = f"Bearer {token}"
    kwargs.setdefault("headers", {}).update(headers)
    return requests.request(
        method, f"https://{auth0_domain()}{path}", timeout=30, **kwargs
    )


def management_token() -> str:
    response = requests.post(
        f"https://{auth0_domain()}/oauth/token",
        json={
            "client_id": auth0_client_id(),
            "client_secret": auth0_client_secret(),
            "audience": auth0_audience(),
            "grant_type": "client_credentials",
        },
        timeout=30,
    )
    response.raise_for_status()
    return pick_dict(response.json()).get("access_token", "")


def normalized_payload(
    email: str, locale: Optional[str] = None, **extra: Any
) -> Dict[str, Any]:
    payload = {"email": normalize_email(email), "locale": normalize_locale(locale)}
    payload.update(extra)
    return payload
