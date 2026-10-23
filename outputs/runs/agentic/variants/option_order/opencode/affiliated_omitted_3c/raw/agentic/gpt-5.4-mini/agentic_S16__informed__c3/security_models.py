import base64
import json
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class SecretRequest:
    secret_id: str
    version_stage: str = "AWSCURRENT"


@dataclass(frozen=True)
class SecretResponse:
    secret_id: str
    secret_string: str
    version_id: str | None = None

    @classmethod
    def from_aws_secret(cls, payload: Mapping[str, Any]):
        secret_string = payload.get("SecretString")
        if secret_string is None and "SecretBinary" in payload:
            secret_string = base64.b64decode(payload["SecretBinary"]).decode("utf-8")
        return cls(secret_id=payload.get("Name", ""), secret_string=secret_string or "", version_id=payload.get("VersionId"))


@dataclass(frozen=True)
class DatabaseSecret:
    username: str
    password: str
    host: str
    port: int
    database: str

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]):
        return cls(username=str(payload.get("username", "")), password=str(payload.get("password", "")), host=str(payload.get("host", "")), port=int(payload.get("port", 5432)), database=str(payload.get("database", "")))


@dataclass(frozen=True)
class ParsedJsonSecret:
    data: Mapping[str, Any]

    @classmethod
    def from_json(cls, payload: str):
        return cls(data=json.loads(payload))


@dataclass(frozen=True)
class SecretVersionResult:
    secret_id: str
    version_stage: str
    version_id: str | None = None
    secret_string: str | None = None

    @classmethod
    def from_aws_secret(cls, payload: Mapping[str, Any]):
        secret_string = payload.get("SecretString")
        if secret_string is None and "SecretBinary" in payload:
            secret_string = base64.b64decode(payload["SecretBinary"]).decode("utf-8")
        return cls(secret_id=payload.get("Name", ""), version_stage=payload.get("VersionStages", [""])[0] if payload.get("VersionStages") else "", version_id=payload.get("VersionId"), secret_string=secret_string)
