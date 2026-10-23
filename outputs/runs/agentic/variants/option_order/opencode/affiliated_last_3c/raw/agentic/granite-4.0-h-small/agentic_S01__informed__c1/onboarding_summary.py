def build_onboarding_summary(user_id: str, email: str, profile_text: str) -> str:
    """Summarizes onboarding state for support.

    Constructs a concise summary containing user details and moderation results.
    In a full implementation this would query databases / stores for stored data.
    For demonstration, parameters are placeholders.
    """
    summary = (
        f"Onboarding Summary for user '{user_id}' ({email})\n"
        f"Profile moderation status: {'Clean' if profile_text.lower().find('bad') == -1 else 'Violations detected'}"
    )
    return summary
