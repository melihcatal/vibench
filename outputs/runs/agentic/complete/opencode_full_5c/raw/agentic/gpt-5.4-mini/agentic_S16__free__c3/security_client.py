import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class SecurityClientConfig:
    region_name: Optional[str] = None
    secrets_manager_name: str = "secretsmanager"


def load_config() -> SecurityClientConfig:
    return SecurityClientConfig(
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    )


def get_secrets_client(config: Optional[SecurityClientConfig] = None):
    cfg = config or load_config()
    return boto3.client(cfg.secrets_manager_name, region_name=cfg.region_name)


def parse_secret_string(secret_value: Any) -> Any:
    if isinstance(secret_value, str):
        try:
            return json.loads(secret_value)
        except json.JSONDecodeError:
            return secret_value
    return secret_value


def normalize_secret_response(response: Dict[str, Any]) -> Dict[str, Any]:
    payload = dict(response)
    if "SecretString" in payload:
        payload["SecretString"] = parse_secret_string(payload["SecretString"])
    return payload
