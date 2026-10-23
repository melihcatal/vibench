import os


def load_identity_config(config=None):
    config = config or {}
    return {
        "api_key": config.get("api_key") or os.getenv("GOOGLE_IDENTITY_TOOLKIT_API_KEY"),
        "provider_id": config.get("provider_id") or os.getenv("GOOGLE_OAUTH_PROVIDER_ID"),
        "tenant_id": config.get("tenant_id") or os.getenv("GOOGLE_IDENTITY_TOOLKIT_TENANT_ID"),
        "redirect_uri": config.get("redirect_uri") or os.getenv("GOOGLE_OAUTH_REDIRECT_URI"),
        "client_id": config.get("client_id") or os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
        "client_secret": config.get("client_secret") or os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    }


def merge_payload(payload=None, config=None):
    data = {}
    if config:
        data.update(config)
    if payload:
        data.update(payload)
    return data
