def onboarding_summary(user_id, email, locale):
    """Summarize onboarding state for support using fabricated data."""
    # In a real implementation you would query your document store, Auth0 user metadata, etc.
    return {
        "user_id": user_id,
        "email": email,
        "locale": locale,
        "summary": "User has completed sign‑up, translation onboarding, and profile moderation. No pending actions." 
    }