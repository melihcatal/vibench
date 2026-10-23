import os
import requests
from http import HTTPStatus
from typing import Any, Dict

class IdentityClient:
    def __init__(self, domain: str, client_id: str, client_secret: str):
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = f'https://{domain}'

    def _request(self, method: str, url: str, json: Dict[str, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
        resp = requests.request(method, self.base_url + url, json=json, headers=self._default_headers(), timeout=10)
        return resp

    def _default_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.client_secret}'
        }

    def post_json(self, url: str, json: Dict[str, Any], headers: Dict[str, str] = None) -> requests.Response:
        return self._request('POST', url, json=json, headers=headers)

    def get_json(self, url: str, params: Dict[str, Any] = None) -> requests.Response:
        resp = requests.get(self.base_url + url, params=params, headers=self._default_headers())
        resp.raise_for_status()
        return resp
