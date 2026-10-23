import os
import json
from anthropic import Anthropic


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def summarize_onboarding_state(onboarding_data: dict) -> str:
    if not ANTHROPIC_API_KEY:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is required for Anthropic Claude inference"
        )

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    data_json = json.dumps(onboarding_data, indent=2, default=str)

    system_prompt = (
        "You are a support assistant. Summarize the onboarding state of a new user account "
        "for a support ticket. Include account creation status, translation locale, moderation "
        "results, and any issues that need attention. Keep it concise and factual."
    )

    user_prompt = f"Onboarding data:\n{data_json}\n\nProvide a summary for support."

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=500,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
    )

    summary = message.content[0].text
    return summary


def generate_support_note(
    onboarding_data: dict, moderation_result: dict = None
) -> dict:
    data_for_summary = dict(onboarding_data)
    if moderation_result:
        data_for_summary["moderation"] = moderation_result

    summary = summarize_onboarding_state(data_for_summary)

    return {
        "summary": summary,
        "user_id": onboarding_data.get("user_id"),
        "email": onboarding_data.get("email"),
        "locale": onboarding_data.get("locale"),
        "model_used": ANTHROPIC_MODEL,
    }
