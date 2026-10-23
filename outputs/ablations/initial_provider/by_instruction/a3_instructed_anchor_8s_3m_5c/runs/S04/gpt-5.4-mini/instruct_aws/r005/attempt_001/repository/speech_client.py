import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    region: str
    bucket: str | None
    role_arn: str | None
    language_code: str


def load_config() -> SpeechConfig:
    return SpeechConfig(
        region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        bucket=os.getenv("AWS_SPEECH_BUCKET"),
        role_arn=os.getenv("AWS_SPEECH_ROLE_ARN"),
        language_code=os.getenv("AWS_TRANSCRIBE_LANGUAGE_CODE", "en-US"),
    )


def s3_uri_from_path(path: str) -> str:
    config = load_config()
    if path.startswith("s3://"):
        return path
    if not config.bucket:
        raise ValueError("AWS_SPEECH_BUCKET is required for local audio paths")
    key = path.lstrip("/")
    return f"s3://{config.bucket}/{key}"
