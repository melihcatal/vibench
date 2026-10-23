from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_get(mapping: Mapping[str, Any], key: str, default: Any = None) -> Any:
    value = mapping.get(key, default)
    return default if value is None else value


@dataclass(frozen=True)
class OnboardingState:
    account_id: str
    email: str
    display_name: Optional[str] = None
    completed_steps: list[str] = field(default_factory=list)
    pending_steps: list[str] = field(default_factory=list)
    last_activity_at: Optional[str] = None
    support_notes: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "OnboardingState":
        return cls(
            account_id=str(_safe_get(data, "account_id", _safe_get(data, "id", ""))),
            email=str(_safe_get(data, "email", "")),
            display_name=_safe_get(data, "display_name"),
            completed_steps=list(_safe_get(data, "completed_steps", [])),
            pending_steps=list(_safe_get(data, "pending_steps", [])),
            last_activity_at=_safe_get(data, "last_activity_at"),
            support_notes=_safe_get(data, "support_notes"),
        )


@dataclass(frozen=True)
class OnboardingSummary:
    summary: str
    risk_level: str
    recommended_next_step: str
    generated_at: str
    provider: str = "openai"
    model: str = OPENAI_MODEL

    def as_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "risk_level": self.risk_level,
            "recommended_next_step": self.recommended_next_step,
            "generated_at": self.generated_at,
            "provider": self.provider,
            "model": self.model,
        }


class OpenAIOnboardingSummarizer:
    def __init__(self, api_key: Optional[str] = None, timeout: int = 30) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required")
        self.timeout = timeout

    def summarize(self, state: OnboardingState) -> OnboardingSummary:
        payload = {
            "model": OPENAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You summarize onboarding state for support teams. Return concise, operational guidance.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Account ID: {state.account_id}\n"
                        f"Email: {state.email}\n"
                        f"Display name: {state.display_name or ''}\n"
                        f"Completed steps: {', '.join(state.completed_steps) or 'none'}\n"
                        f"Pending steps: {', '.join(state.pending_steps) or 'none'}\n"
                        f"Last activity: {state.last_activity_at or 'unknown'}\n"
                        f"Support notes: {state.support_notes or 'none'}\n"
                        "Provide a short support summary, a risk level (low, medium, high), and the best next step."
                    ),
                },
            ],
            "temperature": 0.2,
        }
        response = requests.post(
            OPENAI_CHAT_COMPLETIONS_URL,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        risk_level = self._infer_risk_level(state)
        return OnboardingSummary(
            summary=content,
            risk_level=risk_level,
            recommended_next_step=self._recommended_next_step(state),
            generated_at=_utc_now_iso(),
        )

    def _infer_risk_level(self, state: OnboardingState) -> str:
        if state.pending_steps:
            if len(state.pending_steps) >= 3:
                return "high"
            return "medium"
        return "low"

    def _recommended_next_step(self, state: OnboardingState) -> str:
        if state.pending_steps:
            return f"Complete: {state.pending_steps[0]}"
        if state.support_notes:
            return "Follow up on support notes"
        return "No immediate action needed"


def summarize_onboarding_state(data: Mapping[str, Any], api_key: Optional[str] = None) -> dict[str, Any]:
    state = OnboardingState.from_mapping(data)
    summary = OpenAIOnboardingSummarizer(api_key=api_key).summarize(state)
    return summary.as_dict()
