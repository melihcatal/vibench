import os
from dataclasses import dataclass
from typing import Optional

import google.auth.transport.requests
import google.oauth2.id_token
import requests


@dataclass
class IdentityConfig:
    google_identity_platform_api_key: str
    google_project_id: Optional[str] = None
    default_locale: str = "en"


def load_config() -> IdentityConfig:
    return IdentityConfig(
        google_identity_platform_api_key=os.environ.get("GOOGLE_IDENTITY_PLATFORM_API_KEY", ""),
        google_project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        default_locale=os.environ.get("DEFAULT_LOCALE", "en"),
    )


class GoogleIdentityClient:
    def __init__(self, config: Optional[IdentityConfig] = None) -> None:
        self.config = config or load_config()
        self.session = requests.Session()
        self.request_adapter = google.auth.transport.requests.Request(session=self.session)

    @property
    def key(self) -> str:
        return self.config.google_identity_platform_api_key

    def verify_google_id_token(self, token: str):
        audience = self.config.google_project_id or self.key or None
        return google.oauth2.id_token.verify_oauth2_token(token, self.request_adapter, audience=audience)
