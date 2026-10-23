import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    aws_region: str
    aws_access_key_id: str | None
    aws_secret_access_key: str | None
    aws_session_token: str | None


def load_config() -> SpeechConfig:
    return SpeechConfig(
        aws_region=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
    )


def normalize_uri(uri: str) -> str:
    if uri.startswith("s3://") or uri.startswith("https://") or uri.startswith("http://"):
        return uri
    return f"s3://{uri.lstrip('/')}"
