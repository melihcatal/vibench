from __future__ import annotations

from typing import Any, Dict

from anthropic import Anthropic

from identity_models import OnboardingSummaryRequest


def onboarding_summary(request: OnboardingSummaryRequest | Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(request, dict):
        request = OnboardingSummaryRequest(**request)
    client = Anthropic(api_key=__import__("os").environ.get("ANTHROPIC_API_KEY"))
    prompt = f"Summarize onboarding state for support using the following notes for user {request.user_id}: {dict(request.notes)}"
    message = client.messages.create(model="claude-3-5-sonnet-20240620", max_tokens=300, messages=[{"role": "user", "content": prompt}])
    return {"user_id": request.user_id, "summary": message.content[0].text if message.content else ""}
