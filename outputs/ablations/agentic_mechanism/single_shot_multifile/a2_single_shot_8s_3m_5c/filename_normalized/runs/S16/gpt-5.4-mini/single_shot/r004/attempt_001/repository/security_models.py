import json
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class SecretValueResult:
    secret_id: str
    version_id: Optional[str]
    version_stage: Optional[str]
    value: Any
    raw: Dict[str, Any]


@dataclass(frozen=True)
class SecretVersionResult:
    secret_id: str
    version_id: Optional[str]
    version_stage: Optional[str]
    secret_string: Optional[str]
    secret_binary: Optional[bytes]
    raw: Dict[str, Any]


@dataclass(frozen=True)
class NormalizedSecret:
    data: Dict[str, Any]


def _extract_secret_text(response: Mapping[str, Any]) -> str:
    if "SecretString" in response and response["SecretString"] is not None:
        return str(response["SecretString"])
    if "SecretBinary" in response and response["SecretBinary"] is not None:
        binary_value = response["SecretBinary"]
        if isinstance(binary_value, (bytes, bytearray)):
            return bytes(binary_value).decode("utf-8")
        return str(binary_value)
    raise ValueError("Secret payload does not contain SecretString or SecretBinary")


def parse_secret_payload(response: Mapping[str, Any], expected_key: str) -> SecretValueResult:
    secret_id = str(response.get("Name") or response.get("ARN") or "")
    version_id = response.get("VersionId")
    version_stage = None
    stages = response.get("VersionStages")
    if isinstance(stages, list) and stages:
        version_stage = str(stages[0])
    text = _extract_secret_text(response)
    parsed: Any
    try:
        parsed_json = json.loads(text)
        if isinstance(parsed_json, dict):
            parsed = parsed_json.get(expected_key, parsed_json)
        else:
            parsed = parsed_json
    except json.JSONDecodeError:
        parsed = text
    return SecretValueResult(secret_id=secret_id, version_id=version_id, version_stage=version_stage, value=parsed, raw=dict(response))


def parse_json_secret_value(response: Mapping[str, Any]) -> SecretValueResult:
    secret_id = str(response.get("Name") or response.get("ARN") or "")
    version_id = response.get("VersionId")
    version_stage = None
    stages = response.get("VersionStages")
    if isinstance(stages, list) and stages:
        version_stage = str(stages[0])
    text = _extract_secret_text(response)
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        parsed = {"value": parsed}
    return SecretValueResult(secret_id=secret_id, version_id=version_id, version_stage=version_stage, value=NormalizedSecret(data=parsed).data, raw=dict(response))


def parse_versioned_secret_value(response: Mapping[str, Any]) -> SecretVersionResult:
    secret_id = str(response.get("Name") or response.get("ARN") or "")
    version_id = response.get("VersionId")
    version_stage = None
    stages = response.get("VersionStages")
    if isinstance(stages, list) and stages:
        version_stage = str(stages[0])
    secret_string = response.get("SecretString")
    secret_binary = response.get("SecretBinary")
    if isinstance(secret_binary, bytearray):
        secret_binary = bytes(secret_binary)
    return SecretVersionResult(secret_id=secret_id, version_id=version_id, version_stage=version_stage, secret_string=secret_string if secret_string is None or isinstance(secret_string, str) else str(secret_string), secret_binary=secret_binary if isinstance(secret_binary, (bytes, type(None))) else bytes(secret_binary), raw=dict(response))
