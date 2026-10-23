import os


def load_identity_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.environ["COGNITO_REGION"],
        "domain_prefix": config.get("domain_prefix") or os.environ["COGNITO_DOMAIN_PREFIX"],
        "client_id": config.get("client_id") or os.environ["COGNITO_CLIENT_ID"],
        "client_secret": config.get("client_secret") or os.environ.get("COGNITO_CLIENT_SECRET"),
        "identity_provider": config.get("identity_provider") or os.environ.get("COGNITO_IDENTITY_PROVIDER"),
    }


def merge_payload(payload, config=None):
    merged = load_identity_config(config)
    merged.update(payload or {})
    return merged
