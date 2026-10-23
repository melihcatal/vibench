import os
import requests
from typing import Any, Dict

class IdentityError(Exception):
    """Custom exception for identity service errors."""
    pass

class IdentityClient:
    """
    Thin wrapper around a third‑party identity provider (Auth0 in this example).
    Handles request signing, base URL, error handling, and idempotent call patterns.
    """
    def __init__(self, *, base_url: str, client_id: str, client_secret: str, audience: str, **kwargs: Any):
        self.base_url = base_url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.audience = audience
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self._generate_jwt(),
        }

    def _generate_jwt(self) -> str:
        """Create a JWT for this client using the client secret as a placeholder.",
        "Auth0 expects a client_credentials grant; actual token creation is left to the provider."""
        # Simple token generation for demonstration; real SDKs would use proper crypto.
        import jwt
        import datetime
        payload = {
            "iss": self.client_id,
            "sub": self.client_id,
            "aud": self.audience,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
        }
        return jwt.encode(payload, self.client_secret, algorithm="HS256")

    def _request(self, method: str, path: str, *, json: Any = None, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}{path}"
        if json is not None:
            kwargs.setdefault('json', json)
        kwargs.setdefault('headers', self.headers)
        return requests.request(method, url, **kwargs)

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request('GET', path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request('POST', path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request('DELETE', path, **kwargs)

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        return self._request(method, path, **kwargs)

    def raise_for_status(self, response: requests.Response) -> None:
        if response.status_code >= 400:
            raise IdentityError(f"Identity API error {response.status_code}: {response.text}")
