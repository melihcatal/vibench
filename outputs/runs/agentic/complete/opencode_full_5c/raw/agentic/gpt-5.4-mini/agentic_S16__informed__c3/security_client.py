import os


def get_aws_region() -> str:
    return os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def get_secret_name(name: str) -> str:
    prefix = os.getenv("SECRET_NAME_PREFIX", "")
    return f"{prefix}{name}"
