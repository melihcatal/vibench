import os
import json
import requests
from typing import Optional, Dict, Any
from identity_models import (
    OAuthConfig,
    OAuthClient,
    OAuthResponse,
    OAuthError,
    PKCEHelper,
)


class FederatedIdentityClient:
    def __init__(self):
        self.config = OAuthConfig()
        self.client = OAuthClient(self.config)

    def start_oauth_flow(self, state: str, code_challenge: Optional[str] = None) -> str:
        params = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "scope": self.config.scope,
            "state": state,
        }
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = "S256"
        auth_url = f"{self.config.auth_url}?" + "&".join(
            [f"{k}={v}" for k, v in params.items()]
        )
        return auth_url

    def exchange_code_for_tokens(
        self, code: str, code_verifier: Optional[str] = None
    ) -> OAuthResponse:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.config.redirect_uri,
            "client_id": self.config.client_id,
        }
        if code_verifier:
            data["code_verifier"] = code_verifier
        if self.config.client_secret:
            data["client_secret"] = self.config.client_secret
        response = requests.post(self.config.token_url, data=data)
        if response.status_code != 200:
            error = response.json().get("error", "unknown_error")
            error_description = response.json().get("error_description")
            raise OAuthError(error, error_description)
        tokens = response.json()
        return OAuthResponse(
            access_token=tokens["access_token"],
            id_token=tokens["id_token"],
            refresh_token=tokens.get("refresh_token"),
            expires_in=tokens.get("expires_in"),
        )

    def refresh_access_token(self, refresh_token: str) -> OAuthResponse:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.config.client_id,
        }
        if self.config.client_secret:
            data["client_secret"] = self.config.client_secret
        response = requests.post(self.config.token_url, data=data)
        if response.status_code != 200:
            error = response.json().get("error", "unknown_error")
            error_description = response.json().get("error_description")
            raise OAuthError(error, error_description)
        tokens = response.json()
        return OAuthResponse(
            access_token=tokens["access_token"],
            id_token=tokens.get("id_token"),
            refresh_token=tokens.get("refresh_token"),
            expires_in=tokens.get("expires_in"),
        )
