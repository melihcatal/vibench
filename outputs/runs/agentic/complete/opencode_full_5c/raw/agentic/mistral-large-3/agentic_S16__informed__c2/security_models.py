from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SecretResponse:
    value: str
    name: str
    version: str
    enabled: bool
    expires_on: Optional[str] = None
    created_on: Optional[str] = None
    tags: Optional[Dict[str, str]] = None

    @classmethod
    def from_azure_secret(cls, secret) -> "SecretResponse":
        return cls(
            value=secret.value,
            name=secret.name,
            version=secret.properties.version,
            enabled=secret.properties.enabled,
            expires_on=str(secret.properties.expires_on)
            if secret.properties.expires_on
            else None,
            created_on=str(secret.properties.created_on)
            if secret.properties.created_on
            else None,
            tags=secret.properties.tags,
        )


@dataclass
class DBSecret:
    username: str
    password: str
    host: str
    port: str
    database: str

    @classmethod
    def from_tags_and_value(cls, tags: Dict[str, str], value: str) -> "DBSecret":
        return cls(
            username=tags.get("db_username", ""),
            password=value,
            host=tags.get("db_host", ""),
            port=tags.get("db_port", ""),
            database=tags.get("db_name", ""),
        )
