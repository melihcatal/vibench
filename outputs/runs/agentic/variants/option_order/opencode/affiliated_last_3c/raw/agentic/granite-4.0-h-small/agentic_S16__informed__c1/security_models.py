from __future__ import annotations
import typing
import json
from typing import TypedDict


class SecretRequest(TypedDict):
    name: str
    version: str | None
    staged: bool | None


class SecretResponse(TypedDict):
    value: str
    version: str
    created_at: str
    description: str | None


class NormalizedSecret(TypedDict):
    provider: str
    name: str
    value: str
    metadata: SecretMetadata


def normalize_response(provider: str, raw: dict) -> NormalizedSecret:
    """Convert provider-specific secret response into a unified format."""
    if provider == "azure":
        return {
            "provider": "azure",
            "name": raw["name"],
            "value": raw["value"],
            "metadata": {
                "name": raw["name"],
                "description": raw.get("description"),
                "created_at": raw["created_at"],
            },
        }
    elif provider == "aws":
        secret_string = raw.get("SecretString")
        if secret_string:
            value = secret_string
        else:
            # binary secret, decode base64
            value = base64.b64decode(raw.get("SecretBinary", "")).decode("utf-8")
        return {
            "provider": "aws",
            "name": raw["Name"],
            "value": value,
            "metadata": {
                "name": raw["Name"],
                "description": raw.get("Description"),
                "created_at": raw.get("CreationDate", "").isoformat()
                if isinstance(raw.get("CreationDate"), datetime.datetime)
                else raw.get("CreationDate"),
            },
        }
    elif provider == "google":
        payload = raw["payload"]["data"].decode("utf-8")
        data = json.loads(payload)
        return {
            "provider": "google",
            "name": raw["name"],
            "value": data,
            "metadata": {
                "name": raw["name"],
                "description": raw.get("description"),
                "created_at": raw["createTime"].isoformat()
                if isinstance(raw.get("createTime"), datetime.datetime)
                else raw.get("createTime"),
            },
        }
    elif provider == "doppler":
        return {
            "provider": "doppler",
            "name": raw["name"],
            "value": raw["value"],
            "metadata": {
                "name": raw["name"],
                "description": raw.get("description"),
                "created_at": raw.get("created_at"),
            },
        }
    raise ValueError(f"Unsupported provider normalization: {provider}")
