from typing import TypedDict


# Minimal request model for secret retrieval operations
class GetSecretRequest(TypedDict):
    secret_id: str
    version_stage: str | None = None


# Response model shape – generic for most secret managers
ResponseBase = TypedDict(
    "ResponseBase",
    {
        "SecretString": str | None,
        "SecretBinary": bytes | None,
    },
)

SecretResponse = TypedDict(
    "SecretResponse",
    {
        **ResponseBase.__annotations__,
        # Other provider‑specific keys can be added here as needed
    },
)


# Utilities for normalising responses across providers
# E.g. translate Binary secrets into Unicode strings if possible
def normalise_secret(resp: SecretResponse) -> str | bytes:
    """Return the payload as a string when possible.
    If the secret is binary, leave it as bytes."""
    if resp.get("SecretString"):
        return resp["SecretString"]
    return resp.get("SecretBinary")


# Example: enforce standard field names after normalisation
#   provider  --> standard
#   AccessKey  --> username
#   SecretKey  --> password
#   Endpoint   --> host
#   Port       --> port


def map_to_standard(payload: dict) -> dict:
    standard = {}
    key_map = {
        "AccessKey": "username",
        "SecretKey": "password",
        "Endpoint": "host",
        "Port": "port",
        "Region": "region",
    }
    for src, dest in key_map.items():
        if src in payload:
            standard[dest] = payload[src]
    # Preserve any unknown keys in a raw dict
    standard["_raw"] = {k: v for k, v in payload.items() if k not in key_map}
    return standard
