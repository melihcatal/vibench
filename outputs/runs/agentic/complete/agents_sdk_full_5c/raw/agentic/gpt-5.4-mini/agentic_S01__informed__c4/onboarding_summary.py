from __future__ import annotations

from identity_client import get_identity_client
from identity_models import SummaryRequest


def onboarding_summary(user_id: str, onboarding_state: dict | None = None, locale: str | None = None):
    client = get_identity_client()
    request = SummaryRequest(user_id=user_id, locale=locale, onboarding_state=onboarding_state or {})
    return client.summarize_onboarding(request)
