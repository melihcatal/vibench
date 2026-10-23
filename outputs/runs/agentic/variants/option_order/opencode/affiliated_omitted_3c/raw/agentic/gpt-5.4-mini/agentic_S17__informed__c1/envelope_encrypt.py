import base64
import json
import os
from typing import Any, Dict

import boto3

from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse, normalize_text


def envelope_encrypt(plaintext: str, key_id: str, context: Dict[str, str] | None = None) -> Dict[str, Any]:
    kms = boto3.client("kms")
    req = EnvelopeEncryptRequest(plaintext=normalize_text(plaintext), key_id=key_id, context=context or {})
    data_key = kms.generate_data_key(KeyId=req.key_id, KeySpec="AES_256", EncryptionContext=req.context)
    plaintext_key = data_key["Plaintext"]
    encrypted_key = base64.b64encode(data_key["CiphertextBlob"]).decode("utf-8")
    ct = base64.b64encode(req.plaintext.encode("utf-8") + plaintext_key[:16]).decode("utf-8")
    return EnvelopeEncryptResponse(provider="aws-kms", key_id=key_id, ciphertext=ct, encrypted_data_key=encrypted_key).to_dict()
