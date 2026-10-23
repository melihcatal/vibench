import base64
import json
import os
import sys
import uuid
from typing import Any, Dict, Optional, Tuple

import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


AWS_REGION_ENV = "AWS_REGION"
AWS_KMS_KEY_ID_ENV = "AWS_KMS_KEY_ID"


def _kms_client():
    region = os.environ.get(AWS_REGION_ENV)
    session = boto3.session.Session(region_name=region) if region else boto3.session.Session()
    return session.client("kms")


def _generate_data_key(key_id: Optional[str]) -> Tuple[bytes, bytes, str]:
    kms = _kms_client()
    response = kms.generate_data_key(KeyId=key_id or os.environ.get(AWS_KMS_KEY_ID_ENV), KeySpec="AES_256")
    return response["Plaintext"], response["CiphertextBlob"], response.get("KeyId")


def envelope_encrypt(plaintext: str, key_id: Optional[str] = None, aad: Optional[str] = None) -> Dict[str, Any]:
    data_key_plaintext, data_key_ciphertext, returned_key_id = _generate_data_key(key_id)
    aesgcm = AESGCM(data_key_plaintext)
    nonce = uuid.uuid4().bytes[:12]
    aad_bytes = aad.encode("utf-8") if aad is not None else None
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), aad_bytes)
    return {
        "provider": "aws_kms",
        "envelope_encryption": True,
        "key_id": key_id or os.environ.get(AWS_KMS_KEY_ID_ENV),
        "key_id_returned": returned_key_id,
        "encrypted_data_key_b64": base64.b64encode(data_key_ciphertext).decode("ascii"),
        "nonce_b64": base64.b64encode(nonce).decode("ascii"),
        "ciphertext_b64": base64.b64encode(ciphertext).decode("ascii"),
        "aad": aad,
        "algorithm": "AES-256-GCM",
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return 2
    plaintext = argv[1]
    key_id = argv[2] if len(argv) > 2 else None
    aad = argv[3] if len(argv) > 3 else None
    result = envelope_encrypt(plaintext, key_id=key_id, aad=aad)
    sys.stdout.write(json.dumps(result, separators=(",", ":")))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
