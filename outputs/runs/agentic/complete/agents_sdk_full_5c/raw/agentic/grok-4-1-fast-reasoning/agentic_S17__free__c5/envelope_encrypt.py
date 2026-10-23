import boto3
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from typing import Dict, Any
from security_client import get_aws_region, get_encrypt_key_id
from security_models import CryptoEnvelope, serialize_envelope, normalize_plaintext, serialize_bytes

def envelope_encrypt(plaintext: str) -> str:
    region = get_aws_region()
    key_id = get_encrypt_key_id()
    client = boto3.client('kms', region_name=region)
    plaintext_bytes = normalize_plaintext(plaintext)

    data_key_resp = client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256'
    )
    dek = data_key_resp['Plaintext']
    encrypted_dek = serialize_bytes(data_key_resp['CiphertextBlob'])

    iv = os.urandom(12)
    aesgcm = AESGCM(dek)
    ciphertext = aesgcm.encrypt(iv, plaintext_bytes, None)

    envelope = CryptoEnvelope(
        encrypted_key=encrypted_dek,
        iv=serialize_bytes(iv),
        ciphertext=serialize_bytes(ciphertext)
    )
    return serialize_envelope(envelope)