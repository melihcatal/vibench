import os

from security_client import get_transit, load_security_settings
from security_models import (
    CryptoResult,
    PlaintextPayload,
    build_metadata,
    normalize_key_name,
    normalize_text,
)


def encrypt_payload(plaintext: str, key_name: str) -> CryptoResult:
    payload = PlaintextPayload(
        plaintext=normalize_text(plaintext),
        key_name=normalize_key_name(key_name),
        metadata=build_metadata(operation="encrypt"),
    )
    transit = get_transit()
    response = transit.encrypt_data(name=payload.key_name, plaintext=payload.plaintext)
    return CryptoResult(
        ok=True,
        provider=load_security_settings()["provider"],
        key_name=payload.key_name,
        payload={
            "ciphertext": response["data"]["ciphertext"],
            "plaintext": payload.plaintext,
        },
    )


def main() -> None:
    plaintext = os.getenv("PLAINTEXT", "")
    key_name = os.getenv("KEY_NAME", "transit-key")
    result = encrypt_payload(plaintext, key_name)
    print(result.payload["ciphertext"])


if __name__ == "__main__":
    main()
