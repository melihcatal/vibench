from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import requests

from identity_models import (
    EmailPasswordIdentityRequest,
    EmailPasswordIdentityResponse,
    NoteStoreRequest,
    ModerationRequest,
    SummaryRequest,
    TranslationRequest,
    normalize_metadata,
    normalize_text,
)

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")
AUTH0_MANAGEMENT_BASE = f"https://{AUTH0_DOMAIN}/api/v2"
AUTH0_OIDC_BASE = f"https://{AUTH0_DOMAIN}/oauth/token"

TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY", "")
TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "")

CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "https://example.cognitiveservices.azure.com")
CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

CLOUDANT_URL = os.getenv("IBM_CLOUDANT_URL", "")
CLOUDANT_APIKEY = os.getenv("IBM_CLOUDANT_APIKEY", "")
CLOUDANT_DB = os.getenv("IBM_CLOUDANT_DB", "onboarding_notes")


class Auth0IdentityClient:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _management_token(self) -> str:
        resp = self.session.post(
            AUTH0_OIDC_BASE,
            json={
                "client_id": AUTH0_CLIENT_ID,
                "client_secret": AUTH0_CLIENT_SECRET,
                "audience": AUTH0_AUDIENCE,
                "grant_type": "client_credentials",
            },
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json()["access_token"]

    def _management_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self._management_token()}"}

    def register_user(self, req: EmailPasswordIdentityRequest) -> EmailPasswordIdentityResponse:
        payload = {
            "email": req.normalized_email(),
            "password": req.password,
            "connection": "Username-Password-Authentication",
            "name": req.display_name or req.normalized_email(),
            "user_metadata": normalize_metadata(req.metadata),
        }
        resp = self.session.post(
            f"{AUTH0_MANAGEMENT_BASE}/users",
            json=payload,
            headers=self._management_headers(),
            timeout=20,
        )
        return self._response("auth0", resp)

    def login(self, req: EmailPasswordIdentityRequest) -> EmailPasswordIdentityResponse:
        resp = self.session.post(
            AUTH0_OIDC_BASE,
            json={
                "grant_type": "password",
                "username": req.normalized_email(),
                "password": req.password,
                "audience": AUTH0_AUDIENCE,
                "scope": "openid profile email offline_access",
                "client_id": AUTH0_CLIENT_ID,
            },
            timeout=20,
        )
        return self._response("auth0", resp)

    def refresh_session(self, refresh_token: str) -> EmailPasswordIdentityResponse:
        resp = self.session.post(
            AUTH0_OIDC_BASE,
            json={
                "grant_type": "refresh_token",
                "client_id": AUTH0_CLIENT_ID,
                "refresh_token": refresh_token,
            },
            timeout=20,
        )
        return self._response("auth0", resp)

    def password_reset(self, req: EmailPasswordIdentityRequest) -> EmailPasswordIdentityResponse:
        resp = self.session.post(
            f"{AUTH0_MANAGEMENT_BASE}/tickets/password-change",
            json={
                "email": req.normalized_email(),
                "connection_id": None,
                "client_id": AUTH0_CLIENT_ID,
            },
            headers=self._management_headers(),
            timeout=20,
        )
        return self._response("auth0", resp)

    def translate_copy(self, req: TranslationRequest) -> EmailPasswordIdentityResponse:
        text = normalize_text(req.text)
        url = f"{TRANSLATOR_ENDPOINT}/translate?api-version=3.0&to={req.target_locale}"
        if req.source_locale:
            url += f"&from={req.source_locale}"
        resp = self.session.post(
            url,
            headers={
                "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
                "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION,
                "Content-Type": "application/json",
            },
            json=[{"text": text}],
            timeout=20,
        )
        return self._response("azure-translate", resp)

    def moderate_profile(self, req: ModerationRequest) -> EmailPasswordIdentityResponse:
        resp = self.session.post(
            f"{CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version=2024-09-01",
            headers={
                "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY,
                "Content-Type": "application/json",
            },
            json={"text": normalize_text(req.text), "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]},
            timeout=20,
        )
        return self._response("azure-content-safety", resp)

    def summarize_onboarding(self, req: SummaryRequest) -> EmailPasswordIdentityResponse:
        import json

        prompt = json.dumps({"user_id": req.user_id, "locale": req.locale, "state": req.onboarding_state}, ensure_ascii=False)
        resp = self.session.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": "Summarize onboarding state for support in concise, neutral language."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
            },
            timeout=30,
        )
        return self._response("openai", resp)

    def store_note(self, req: NoteStoreRequest) -> EmailPasswordIdentityResponse:
        if not CLOUDANT_URL:
            return EmailPasswordIdentityResponse(ok=False, provider="cloudant", error="IBM_CLOUDANT_URL not configured")
        session = requests.Session()
        session.auth = ("apikey", CLOUDANT_APIKEY)
        session.headers.update({"Content-Type": "application/json"})
        db_url = f"{CLOUDANT_URL.rstrip('/')}/{CLOUDANT_DB}"
        resp = session.post(
            db_url,
            json={"user_id": req.user_id, "note": normalize_text(req.note), "metadata": normalize_metadata(req.metadata)},
            timeout=20,
        )
        return self._response("cloudant", resp)

    def _response(self, provider: str, resp: requests.Response) -> EmailPasswordIdentityResponse:
        try:
            data: Dict[str, Any] = resp.json()
        except Exception:
            data = {"text": resp.text}
        ok = 200 <= resp.status_code < 300
        return EmailPasswordIdentityResponse(ok=ok, provider=provider, data=data, error=None if ok else data.get("error_description") or data.get("message") or resp.text)


def get_identity_client() -> Auth0IdentityClient:
    return Auth0IdentityClient()
