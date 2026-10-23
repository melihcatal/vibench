def normalize_identity_profile(profile):
    profile = profile or {}
    return {
        "subject": profile.get("sub") or profile.get("id") or profile.get("user_id"),
        "email": profile.get("email"),
        "email_verified": bool(profile.get("email_verified")),
        "display_name": profile.get("name") or profile.get("preferred_username") or profile.get("nickname"),
        "given_name": profile.get("given_name"),
        "family_name": profile.get("family_name"),
        "raw": profile,
    }
