import os


def load_config(config=None):
    base = dict(config or {})
    if "region" not in base and os.getenv("AWS_REGION"):
        base["region"] = os.getenv("AWS_REGION")
    if "secret_name" not in base and os.getenv("SECRET_NAME"):
        base["secret_name"] = os.getenv("SECRET_NAME")
    if "version_stage" not in base and os.getenv("SECRET_VERSION_STAGE"):
        base["version_stage"] = os.getenv("SECRET_VERSION_STAGE")
    if "version_id" not in base and os.getenv("SECRET_VERSION_ID"):
        base["version_id"] = os.getenv("SECRET_VERSION_ID")
    return base


def normalize_secret_value(response):
    if "SecretString" in response:
        return response["SecretString"]
    return response["SecretBinary"].decode("utf-8")


def secret_identifier(payload):
    return payload.get("secret_id") or payload.get("secret_name")
