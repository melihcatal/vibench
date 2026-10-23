import os

from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

from security_client import get_managed_key
from security_models import CryptoResponse, b64d, normalize_text


def decrypt_payload(
    ciphertext: str, key_name: str, algorithm: str = "RSA-OAEP"
) -> CryptoResponse:
    key = get_managed_key(key_name)
    client = CryptographyClient(key, key.client)
    result = client.decrypt(EncryptionAlgorithm.rsa_oaep, b64d(ciphertext))
    return CryptoResponse(
        key_id=key.id,
        algorithm=algorithm,
        plaintext=normalize_text(result.plaintext),
        metadata={"provider": "azure-key-vault-keys"},
    )


def main() -> None:
    ciphertext = os.environ.get("CIPHERTEXT", "")
    key_name = os.environ.get("KEY_NAME", "")
    if not ciphertext or not key_name:
        raise ValueError("CIPHERTEXT and KEY_NAME are required")
    decrypt_payload(ciphertext, key_name)


if __name__ == "__main__":
    main()
