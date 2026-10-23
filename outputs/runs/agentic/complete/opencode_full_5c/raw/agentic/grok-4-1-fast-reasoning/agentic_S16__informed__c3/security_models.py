from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class SecretRequest:
    name: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


@dataclass
class SecretResponse:
    secret_string: Optional[str] = None
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    arn: Optional[str] = None


def parse_secret_response(raw: Dict[str, Any]) -> SecretResponse:
    return SecretResponse(
        secret_string=raw.get("SecretString"),
        version_id=raw.get("VersionId"),
        version_stage=raw.get("VersionStage"),
        arn=raw.get("ARN"),
    )
