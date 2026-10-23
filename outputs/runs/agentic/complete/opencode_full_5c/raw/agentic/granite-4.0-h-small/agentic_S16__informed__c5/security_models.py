import os
from typing import TypedDict


class Secret(TypedDict):
    secret_id: str
    version: int | str


class SecretConfig(TypedDict):
    secret: Secret | dict
    metadata: dict


def normalize_secret_response(raw: dict) -> SecretConfig:
    """Normalize raw secret manager responses to a common schema.

    Expected keys: secret_id, version, secret (raw payload), metadata.
    """
    return {
        "secret": raw.get("secret") or raw,
        "metadata": raw.get("metadata", {}),
    }
