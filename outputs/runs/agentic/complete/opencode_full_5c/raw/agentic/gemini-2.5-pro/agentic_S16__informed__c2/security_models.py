from dataclasses import dataclass


@dataclass
class SecretPayload:
    name: str
    value: str
    version: str | None = None
    arn: str | None = None
