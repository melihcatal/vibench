import os
from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityConfig:
    aws_region: str
    secret_id: str


def load_security_config(secret_id: str | None = None) -> SecurityConfig:
    return SecurityConfig(
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
        secret_id=secret_id or os.getenv("SECRET_ID", "example/secret"),
    )


def secret_name_for(label: str) -> str:
    return f"{label}-secret"
