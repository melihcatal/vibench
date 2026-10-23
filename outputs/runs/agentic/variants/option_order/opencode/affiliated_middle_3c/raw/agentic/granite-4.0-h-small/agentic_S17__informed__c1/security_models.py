import os
from typing import TypedDict

# Request and response models for encryption and signing operations

Status = TypedDict("Status", {"code": int, "message": str})

EncryptRequest = TypedDict(
    "EncryptRequest",
    {
        "key_name": str,
        "plaintext": str,
    },
)

EncryptResponse = TypedDict(
    "EncryptResponse",
    {
        "ciphertext": str,
        "status": Status,
    },
)

DecryptRequest = TypedDict(
    "DecryptRequest",
    {
        "ciphertext": str,
        "key_name": str,
    },
)

DecryptResponse = TypedDict(
    "DecryptResponse",
    {
        "plaintext": str,
        "status": Status,
    },
)

DeKRequest = TypedDict(
    "DeKRequest",
    {
        "encrypted_data_key": str,
        "key_name": str,
    },
)

DeKResponse = TypedDict(
    "DeKResponse",
    {
        "data_key": str,
        "status": Status,
    },
)

SignRequest = TypedDict(
    "SignRequest",
    {
        "key_name": str,
        "data": str,
    },
)

SignResponse = TypedDict(
    "SignResponse",
    {
        "signature": str,
        "status": Status,
    },
)

VerifyRequest = TypedDict(
    "VerifyRequest",
    {
        "key_name": str,
        "signed_data": str,
        "signature": str,
    },
)

VerifyResponse = TypedDict(
    "VerifyResponse",
    {
        "valid": bool,
        "status": Status,
    },
)


# Normalization helpers
def to_dict(obj: TypedDict) -> dict:
    """Convert TypedDict to plain dict for API payloads."""
    return dict(obj)


if __name__ == "__main__":
    # placeholder to ensure no syntax errors
    print("security_models loaded")
