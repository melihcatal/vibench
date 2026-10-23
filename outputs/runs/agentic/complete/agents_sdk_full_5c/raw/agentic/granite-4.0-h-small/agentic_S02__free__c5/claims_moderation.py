import identity_models

# Example moderation: flag or rewrite suspicious free‑text claims
SUSPICIOUS_KEYWORDS = ["hack", "phish", "malware", "spam"]

# Simple moderation policy: truncate claim if it contains suspicious words

def moderate_claim(claim: str) -> str:
    lower = claim.lower()
    if any(k in lower for k in SUSPICIOUS_KEYWORDS):
        # Record that moderation happened (could be logged) and return a clean version
        return "[MODERATED]"
    # Otherwise keep original (trim whitespace for safety)
    return claim.strip()

# Apply moderation to a batch of profile claims

def moderate_profile(profile: dict) -> dict:
    for key in ["name", "bio", "notes", "comments"]:
        if key in profile:
            profile[key] = moderate_claim(profile[key])
    return profile

# Example adapter for federation providers (Auth0, Okta, Google)
def moderate_from_provider(provider_name: str, raw_claims: dict):
    mapped = identity_models.UserProfile.from_generic(raw_claims)
    return moderate_profile(mapped.__dict__)

if __name__ == "__main__":
    # Demo
    pass