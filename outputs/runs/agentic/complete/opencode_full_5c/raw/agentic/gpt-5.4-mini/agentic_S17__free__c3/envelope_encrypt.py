import os

from cryptography.fernet import Fernet

from security_client import (
    derive_data_key,
    get_transit,
    load_security_settings,
    to_base64_text,
)
from security_models import (
    EnvelopePayload,
    build_metadata,
    normalize_key_name,
    normalize_text,
)


def envelope_encrypt(plaintext: str, key_name: str) -> EnvelopePayload:
    key = derive_data_key()
    fernet = Fernet(key)
    ciphertext = fernet.encrypt(normalize_text(plaintext).encode("utf-8"))
    transit = get_transit()
    wrapped_key = transit.encrypt_data(
        name=normalize_key_name(key_name), plaintext=to_base64_text(key)
    )
    return EnvelopePayload(
        encrypted_key=wrapped_key["data"]["ciphertext"],
        ciphertext=to_base64_text(ciphertext),
        key_name=normalize_key_name(key_name),
        metadata=build_metadata(
            provider=load_security_settings()["provider"], operation="envelope_encrypt"
        ),
    )


def main() -> None:
    plaintext = os.getenv("PLAINTEXT", "")
    key_name = os.getenv("KEY_NAME", "transit-key")
    result = envelope_encrypt(plaintext, key_name)
    print(result.encrypted_key)
    print(result.ciphertext)


if __name__ == "__main__":
    main()
