import os
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

from security_client import get_managed_key
from security_models import (
    CryptoRequest,
    CryptoResponse,
    b64e,
    normalize_context,
    normalize_text,
)


def encrypt_payload(
    plaintext: str, key_name: str, algorithm: str = "RSA-OAEP"
) -> CryptoResponse:
    key = get_managed_key(key_name)
    client = CryptographyClient(key, key.client)
    request = CryptoRequest(
        key_id=key.id, plaintext=normalize_text(plaintext), algorithm=algorithm
    )
    result = client.encrypt(
        EncryptionAlgorithm.rsa_oaep, request.plaintext.encode("utf-8")
    )
    return CryptoResponse(
        key_id=request.key_id,
        algorithm=algorithm,
        ciphertext=b64e(result.ciphertext),
        metadata={"provider": "azure-key-vault-keys"},
    )


def main() -> None:
    plaintext = os.environ.get("PLAINTEXT", "")
    key_name = os.environ.get("KEY_NAME", "")
    if not plaintext or not key_name:
        raise ValueError("PLAINTEXT and KEY_NAME are required")
    encrypt_payload(plaintext, key_name)


if __name__ == "__main__":
    main()
