import os
import requests
from identity_client import IdentityClient
from identity_models import WelcomePayload, WelcomeResult

# Third‑party translation SaaS (e.g., LingoTranslate API)
BASE_URL = os.getenv(
    "TRANSLATION_SERVICE_URL", "https://api.lingotranslate.example.com"
)
API_KEY = os.getenv("TRANSLATION_SERVICE_API_KEY")


class TranslationClient(IdentityClient):
    """Reuses IdentityClient but points at the translation provider.
    In production the base URL and auth scheme differ, but the HTTP wrapper stays the same.
    """

    pass  # No extra code needed; reuse post/get methods


def translate_onboarding(locale: str, source_text: str) -> WelcomeResult:
    """Translate welcome/onboarding copy into the user's locale.
    Returns a WelcomeResult containing translated strings or an error message.
    """
    payload = WelcomePayload(text=source_text, target_locale=locale).to_dict()
    client = TranslationClient(base_url=BASE_URL, api_key=API_KEY)
    response = client.post("/v1/translate", json=payload)
    data = response.json()
    # Provider returns either translated copy or an error field
    if "error" in data:
        raise RuntimeError(f"Translation service error: {data['error']}")
    return WelcomeResult.from_dict(data)


# ---------------------------------------------------------------------------
# DTOs for the translation provider
# ---------------------------------------------------------------------------
class WelcomePayload:
    def __init__(self, text: str, target_locale: str):
        self.text = text
        self.target_locale = target_locale

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "target_locale": self.target_locale}


class WelcomeResult:
    def __init__(self, translated: str):
        self.translated = translated

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WelcomeResult:
        # Expected key may be `translated` or `translation`
        return cls(translated=data.get("translated") or data.get("translation"))
