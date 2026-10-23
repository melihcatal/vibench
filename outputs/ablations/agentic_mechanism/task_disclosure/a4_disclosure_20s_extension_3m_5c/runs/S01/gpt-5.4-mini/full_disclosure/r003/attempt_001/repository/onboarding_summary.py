import os
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

from openai import OpenAI


@dataclass
class OnboardingSummary:
    user_id: Optional[str]
    email: Optional[str]
    locale: Optional[str]
    account_status: Optional[str]
    profile_status: Optional[str]
    verification_status: Optional[str]
    pending_actions: List[str]
    support_flags: List[str]
    notes: List[str]
    provider: str = "openai/gpt-5.4-mini"


def _normalize_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str):
        return [part.strip() for part in value.splitlines() if part.strip()]
    return [str(value)]


def summarize_onboarding_state(state: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = {
        "role": "user",
        "content": (
            "Summarize this onboarding state for support in concise bullet points. "
            "Return JSON with keys: user_id, email, locale, account_status, profile_status, "
            "verification_status, pending_actions, support_flags, notes. State: "
            f"{state}"
        ),
    }
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[prompt],
        text={"format": {"type": "json_object"}},
    )
    data = response.output_text
    return {
        "summary": data,
        "source": asdict(
            OnboardingSummary(
                user_id=state.get("user_id"),
                email=state.get("email"),
                locale=state.get("locale"),
                account_status=state.get("account_status"),
                profile_status=state.get("profile_status"),
                verification_status=state.get("verification_status"),
                pending_actions=_normalize_list(state.get("pending_actions")),
                support_flags=_normalize_list(state.get("support_flags")),
                notes=_normalize_list(state.get("notes")),
            )
        ),
    }
