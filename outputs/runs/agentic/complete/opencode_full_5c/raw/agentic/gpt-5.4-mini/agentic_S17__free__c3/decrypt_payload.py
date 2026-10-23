import os

from security_client import get_transit, load_security_settings
from security_models import (
    CiphertextPayload,
    CryptoResult,
    build_metadata,
    normalize_key_name,
    normalize_text,
)


def decrypt_payload(ciphertext: str, key_name: str) -> CryptoResult:
    payload = CiphertextPayload(
        ciphertext=normalize_text(ciphertext),
        key_name=normalize_key_name(key_name),
        metadata=build_metadata(operation="decrypt"),
    )
    transit = get_transit()
    response = transit.decrypt_data(
        name=payload.key_name, ciphertext=payload.ciphertext
    )
    return CryptoResult(
        ok=True,
        provider=load_security_settings()["provider"],
        key_name=payload.key_name,
        payload={
            "plaintext": response["data"]["plaintext"],
            "ciphertext": payload.ciphertext,
        },
    )


def main() -> None:
    ciphertext = os.getenv("CIPHERTEXT", "")
    key_name = os.getenv("KEY_NAME", "transit-key")
    result = decrypt_payload(ciphertext, key_name)
    print(result.payload["plaintext"])


if __name__ == "__main__":
    main()
