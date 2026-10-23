import boto3
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from security_client import get_kms_config
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse
from botocore.exceptions import ClientError


def envelope_encrypt(req: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    config = get_kms_config()
    kms_client = boto3.client("kms", **config)
    data_key_response = kms_client.generate_data_key(
        KeyId=req.key_id, KeySpec="AES_256_GCM"
    )
    plaintext_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]
    aesgcm = AESGCM(plaintext_key)
    iv = os.urandom(12)
    ct_tag = aesgcm.encrypt(iv, req.plaintext, None)
    ciphertext = ct_tag[:-16]
    tag = ct_tag[-16:]
    return EnvelopeEncryptResponse(
        encrypted_data_key=encrypted_data_key,
        ciphertext=ciphertext,
        iv=iv,
        tag=tag,
        key_id=req.key_id,
    )
