import json
from identity_models import NormalizedUser


def summarize_onboarding(user: NormalizedUser) -> str:
    """Creates a support-friendly summary of onboarding state.

    Returns a concise JSON string containing username, email, signup date (if any),
    and a list of pending actions (e.g., profile moderation, password reset).
    """
    signup_info = user.get("Attributes", [])
    # Find signup timestamp attribute if present (e.g., 'created_date')
    created = next(
        (a["Value"] for a in signup_info if a["Name"].lower() == "created_date"), None
    )
    pending = [
        "profile moderation"
        if any(a["Name"].lower() == "moderation_pending" for a in user["Attributes"])
        else None,
        "password reset"
        if any(a["Name"].lower() == "reset_pending" for a in user["Attributes"])
        else None,
    ]
    pending = [p for p in pending if p]
    summary = {
        "username": user.get("Username"),
        "email": next(
            (a["Value"] for a in user["Attributes"] if a["Name"].lower() == "email"),
            None,
        ),
        "created_at": created,
        "pending_actions": pending,
    }
    return json.dumps(summary, indent=2)
