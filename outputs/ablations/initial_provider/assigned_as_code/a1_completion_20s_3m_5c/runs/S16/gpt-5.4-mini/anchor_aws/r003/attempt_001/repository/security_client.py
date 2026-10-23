import os


def load_secret_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "secret_id": config.get("secret_id"),
        "version_stage": config.get("version_stage"),
        "version_id": config.get("version_id"),
    }


def normalize_secret_text(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value
