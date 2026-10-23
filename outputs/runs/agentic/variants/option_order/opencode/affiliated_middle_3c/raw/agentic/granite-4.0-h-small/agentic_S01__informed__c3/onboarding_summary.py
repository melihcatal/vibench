def generate_onboarding_summary(onboarding_log: dict) -> str:
    """Summarize onboarding state for support.

    Args:
        onboarding_log: dict containing keys like 'signup_ts', 'locale', 'profile_text', 'verified_emails', etc.

    Returns:
        A concise human‑readable summary.
    """
    summary = [
        f"User created on {onboarding_log.get('signup_ts', 'N/A')} (locale: {onboarding_log.get('locale', 'N/A')})",
        f"Profile text: {onboarding_log.get('profile_text', 'none')} (moderation: {'clean' if moderate_profile(onboarding_log.get('profile_text', '')) else 'flagged'})",
        f"Emails verified: {onboarding_log.get('emails_verified', [])}",
    ]
    return "\\n".join(summary)


def moderate_profile(profile_text: str) -> bool:
    """Thin wrapper to call profile_moderation for reuse."""
    from profile_moderation import moderate_profile_text

    return not bool(moderate_profile_text(profile_text))  # empty = flagged
