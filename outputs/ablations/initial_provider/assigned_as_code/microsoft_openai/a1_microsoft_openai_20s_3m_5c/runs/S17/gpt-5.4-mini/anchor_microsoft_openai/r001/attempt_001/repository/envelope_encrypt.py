from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

from security_models import pack_ciphertext, normalize_bytes


def envelope_encrypt(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config["key_id"], credential=credential) as client:
            key_wrap = client.wrap_key(EncryptionAlgorithm.rsa_oaep_256, normalize_bytes(payload["data_key"]))
            return {
                "wrapped_key": key_wrap.encrypted_key,
                "key_id": key_wrap.key_id,
                "algorithm": "RSA-OAEP-256",
                "encrypted_payload": pack_ciphertext(
                    payload.get("ciphertext"),
                    payload.get("iv"),
                    payload.get("tag"),
                    key_wrap.key_id,
                    "A256GCM",
                ),
            }
