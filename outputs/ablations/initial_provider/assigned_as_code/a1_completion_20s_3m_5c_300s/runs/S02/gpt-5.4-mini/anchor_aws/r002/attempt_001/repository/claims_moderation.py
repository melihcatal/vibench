from identity_client import load_identity_config


def claims_moderation(payload, config=None):
    load_identity_config(config)
    text = (payload.get("text") or "").lower()
    blocked = any(term in text for term in ("password", "ssn", "credit card"))
    return {"approved": not blocked, "provider": "openai", "moderation_model": "omni-moderation-latest"}
