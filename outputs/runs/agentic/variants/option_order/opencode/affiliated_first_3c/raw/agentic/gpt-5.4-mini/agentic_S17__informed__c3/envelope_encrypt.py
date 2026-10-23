import os
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

from security_client import get_managed_key
from security_models import CryptoResponse, b64e


def envelope_encrypt(plaintext: str, key_name: str) -> CryptoResponse:
    key = get_managed_key(key_name)
    client = CryptographyClient(key, key.client)
    aes_key = os.urandom(32)
    iv = os.urandom(12)
    wrapped = client.wrap_key(EncryptionAlgorithm.rsa_oaep, aes_key)
    payload = plaintext.encode("utf-8")
    ciphertext = bytes(a ^ aes_key[i % len(aes_key)] for i, a in enumerate(payload))
    return CryptoResponse(
        key_id=key.id,
        wrapped_key=b64e(wrapped.encrypted_key),
        iv=b64e(iv),
        ciphertext=b64e(ciphertext),
        metadata={"provider": "azure-key-vault-keys", "mode": "envelope"},
    )


if __name__ == "__main__":
    envelope_encrypt(os.environ.get("PLAINTEXT", ""), os.environ.get("KEY_NAME", ""))
