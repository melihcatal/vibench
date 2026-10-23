import os
import requests
from identity_client import IdentityClient
from identity_models import ModerationRequest, ModerationResult

# Provider: Content moderation SaaS (e.g., SafeGuard API)
BASE_URL = os.getenv("MODERATION_SERVICE_URL", "https://api.safeguard.example.com")
API_KEY = os.getenv("MODERATION_SERVICE_API_KEY")


class ModerationClient(IdentityClient):
    """Simple wrapper pointing at the moderation service."""

    pass  # reuse generic http methods


def moderate_profile_text(user_id: str, text: str, locale: str) -> ModerationResult:
    """Run profile text through moderation before account activation.
    Returns a ModerationResult indicating approval status and sanitized content.
    """
    payload = ModerationRequest(user_id=user_id, content=text, locale=locale).to_dict()
    client = ModerationClient(base_url=BASE_URL, api_key=API_KEY)
    response = client.post("/v1/moderate", json=payload)
    data = response.json()
    if response.status_code >= 400:
        raise RuntimeError(
            f"Moderation service error: {data.get('message', 'unknown')}"
        )
    return ModerationResult.from_dict(data)


# ---------------------------------------------------------------------------
# Data models for the moderation provider
# ---------------------------------------------------------------------------
class ModerationRequest:
    def __init__(self, user_id: str, content: str, locale: str, **extra):
        self.user_id = user_id
        self.content = content
        self.locale = locale
        self.extra = extra

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "user_id": self.user_id,
            "content": self.content,
            "locale": self.locale,
        }
        payload.update(self.extra)
        return payload


class ModerationResult:
    def __init__(self, is_approved: bool, safe_content: Optional[str] = None):
        self.is_approved = is_approved
        self.safe_content = safe_content

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ModerationResult:
        return cls(
            is_approved=data.get("approved", False),
            safe_content=data.get("clean_content"),
        )
