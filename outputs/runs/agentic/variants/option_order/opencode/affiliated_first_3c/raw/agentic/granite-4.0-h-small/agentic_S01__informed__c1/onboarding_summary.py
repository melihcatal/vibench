def summarize_onboarding_state(user_id: str, profile: dict, notes: list) -> str:
    """Summarize onboarding state for support agents."""
    summary = f"User {user_id} onboarding summary:\n\n"
    summary += f"Profile: {profile.get('bio', 'No bio provided')}\n"
    summary += f"Notes: {\n        ', '.join(notes) if notes else 'No notes recorded'\n    }\n"
    return summary
