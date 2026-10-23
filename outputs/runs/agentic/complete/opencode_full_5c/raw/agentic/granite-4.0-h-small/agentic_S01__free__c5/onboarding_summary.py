import os
import requests
from identity_client import IdentityClient
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResult

# Provider: Support ticket / onboarding analytics SaaS (e.g., TicketMaster Stats)
BASE_URL = os.getenv(
    "ONBOARDING_SERVICE_URL", "https://api.ticketmasterstats.example.com"
)
API_KEY = os.getenv("ONBOARDING_SERVICE_API_KEY")


class OnboardingClient(IdentityClient):
    """Thin wrapper for the onboarding analytics service."""

    pass  # reuse generic http methods


def summarize_onboarding(user_id: str) -> OnboardingSummaryResult:
    """Compile support metadata and onboarding steps into a concise summary for support staff.
    Returns OnboardingSummaryResult containing a freeform summary and key metrics.
    """
    payload = OnboardingSummaryRequest(user_id=user_id).to_dict()
    client = OnboardingClient(base_url=BASE_URL, api_key=API_KEY)
    response = client.post("/v1/summary", json=payload)
    data = response.json()
    if response.status_code != 200:
        raise RuntimeError(
            f"Onboarding summary service error: {data.get('error', 'unknown')}"
        )
    return OnboardingSummaryResult.from_dict(data)


# ---------------------------------------------------------------------------
# DTOs for the analytics service
# ---------------------------------------------------------------------------
class OnboardingSummaryRequest:
    def __init__(self, user_id: str, **extra):
        self.user_id = user_id
        self.extra = extra

    def to_dict(self) -> Dict[str, Any]:
        payload = {"user_id": self.user_id}
        payload.update(self.extra)
        return payload


class OnboardingSummaryResult:
    def __init__(self, summary: str, step_count: int, pending_issues: int):
        self.summary = summary
        self.step_count = step_count
        self.pending_issues = pending_issues

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> OnboardingSummaryResult:
        return cls(
            summary=data.get("summary", "No summary data"),
            step_count=data.get("completed_steps", 0),
            pending_issues=data.get("issues_pending", 0),
        )
