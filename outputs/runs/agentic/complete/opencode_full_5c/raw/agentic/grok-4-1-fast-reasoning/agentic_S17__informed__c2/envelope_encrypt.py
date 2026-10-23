import os
import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from security_client import get_kms_client
from typing import Dict, Any, Optional


def envelope_encrypt(
    plaintext: bytes, key_id: str, region: Optional[str] = None
) -> Dict[str, Any]:
    client = get_kms_client(region)
    data_key_resp = client.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    plaintext_key = data_key_resp["Plaintext"]
    encrypted_key = data_key_resp["CiphertextBlob"]
    aesgcm = AESGCM(plaintext_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return {"encrypted_key": encrypted_key, "nonce": nonce, "ciphertext": ciphertext}
