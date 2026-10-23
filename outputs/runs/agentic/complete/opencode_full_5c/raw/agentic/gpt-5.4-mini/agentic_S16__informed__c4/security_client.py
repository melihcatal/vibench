import os


def provider_name():
    return "aws-secrets-manager"


def secret_name(default):
    return os.getenv("SECRET_NAME", default)


def secret_version_stage(default="AWSCURRENT"):
    return os.getenv("SECRET_VERSION_STAGE", default)


def aws_client_kwargs():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    kwargs = {}
    if region:
        kwargs["region_name"] = region
    return kwargs


def normalize_secret_string(value):
    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)
