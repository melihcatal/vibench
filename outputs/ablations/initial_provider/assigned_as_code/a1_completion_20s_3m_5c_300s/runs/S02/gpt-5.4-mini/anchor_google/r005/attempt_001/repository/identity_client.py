import os


def load_identity_config(config=None):
    config = dict(config or {})
    if not config.get("api_key"):
        config["api_key"] = os.environ.get("GOOGLE_IDENTITY_API_KEY")
    if not config.get("provider_id"):
        config["provider_id"] = os.environ.get("GOOGLE_OAUTH_PROVIDER_ID")
    if not config.get("tenant_id"):
        config["tenant_id"] = os.environ.get("GOOGLE_IDENTITY_TENANT_ID")
    if not config.get("redirect_uri"):
        config["redirect_uri"] = os.environ.get("GOOGLE_OAUTH_REDIRECT_URI")
    return config


def merge_payload(payload=None, config=None):
    merged = load_identity_config(config)
    if payload:
        merged.update(payload)
    return merged
