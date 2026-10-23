from typing import TypedDict

class SecretDef(TypedDict):
    name: str
    version_stage: str
    provider: str

def normalize_secret(secret_def: dict) -> SecretDef:
    """Normalize a raw secret definition dict into a TypedDict."""
    return {
        "name": secret_def.get("name"),
        "version_stage": secret_def.get("version_stage", "AWSCURRENT"),
        "provider": secret_def.get("provider", "aws")
    }
