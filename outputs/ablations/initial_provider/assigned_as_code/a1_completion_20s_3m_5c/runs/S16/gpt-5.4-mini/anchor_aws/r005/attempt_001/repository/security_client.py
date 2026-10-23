import os


def load_config(config=None):
    base = dict(config or {})
    base.setdefault("region", os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    base.setdefault("version_stage", os.getenv("SECRET_VERSION_STAGE"))
    base.setdefault("version_id", os.getenv("SECRET_VERSION_ID"))
    return base


def secret_string(response):
    if "SecretString" in response:
        return response["SecretString"]
    return response["SecretBinary"].decode("utf-8")
