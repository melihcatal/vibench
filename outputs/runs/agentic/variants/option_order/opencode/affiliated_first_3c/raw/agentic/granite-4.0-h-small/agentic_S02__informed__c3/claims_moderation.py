import json
from identity_models import FederatedProfile, PersistedAuditRecord

# Example moderation policy: reject claims containing prohibited keywords (simple demo)
BANNED_KEYWORDS = {
    "spam",
    "phish",
    "malware",
    "hate",
    "abuse",
    "illegal",
}


def moderate_free_text_claims(profile: FederatedProfile) -> FederatedProfile:
    """Remove or sanitize claims that contain prohibited content."""
    # Demonstration: only moderate `name` and `extra` fields
    if profile.name and any(
        kw.lower() in profile.name.lower() for kw in BANNED_KEYWORDS
    ):
        # Replace offensive name with a placeholder
        moderated_name = "[MODERATED_NAME]"
    else:
        moderated_name = profile.name

    moderated_extra = {}
    if profile.extra:
        for key, value in profile.extra.items():
            if isinstance(value, str) and any(
                kw.lower() in value.lower() for kw in BANNED_KEYWORDS
            ):
                moderated_extra[key] = "[MODERATED]"
            else:
                moderated_extra[key] = value
    # Return a new normalized profile with moderated values
    return FederatedProfile(
        sub=profile.sub,
        name=moderated_name,
        email=profile.email,
        email_verified=profile.email_verified,
        picture=profile.picture,
        extra=moderated_extra,
    )


# Example usage with audit enrichment
if __name__ == "__main__":
    demo_profile = FederatedProfile(
        sub="u_1234",
        name="John Doe",
        email="john@example.com",
        email_verified=True,
        picture="http://example.com/pic.jpg",
        extra={"bio": "Developer at Example", "notes": "Check out spammylink.com"},
    )
    moderated = moderate_free_text_claims(demo_profile)
    audit_entry = PersistedAuditRecord(
        user_sub=moderated.sub,
        event_type="claims_moderation",
        details={
            "original": json.loads(demo_profile.__repr__()),
            "moderated": json.loads(moderated.__repr__()),
        },
        timestamp=datetime.utcnow().isoformat() + "Z",
    )
    # In a real system you would persist `audit_entry` in the managed store
    print("Moderated profile audit entry:", json.dumps(audit_entry._asdict(), indent=2))
