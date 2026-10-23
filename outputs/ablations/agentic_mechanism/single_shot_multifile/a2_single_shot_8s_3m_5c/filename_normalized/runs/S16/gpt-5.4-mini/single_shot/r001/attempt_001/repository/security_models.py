import json
from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class SecretValue:
    name: str
    version: str
    value: str


@dataclass(frozen=True)
class DatabaseSecret:
    name: str
    version: str
    host: str
    port: int
    username: str
    password: str
    database: str


@dataclass(frozen=True)
class SecretVersionRead:
    name: str
    version: str
    value: str


def parse_json_secret_payload(payload: str) -> Dict[str, Any]:
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError("JSON secret must decode to an object")
    return data


def parse_database_secret(payload: str, secret_name: str, version: str) -> DatabaseSecret:
    data = parse_json_secret_payload(payload)
    return DatabaseSecret(
        name=secret_name,
        version=version,
        host=str(data["host"]),
        port=int(data.get("port", 5432)),
        username=str(data["username"]),
        password=str(data["password"]),
        database=str(data.get("database", data.get("dbname", ""))),
    )
