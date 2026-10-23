import base64
import os
from typing import Dict, Optional

import boto3

from security_models import normalize_context, normalize_payload


class SecurityClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = (
            region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
        )
        self.kms = boto3.client("kms", region_name=self.region_name)

    def encrypt(
        self, key_id: str, payload: str, context: Optional[Dict[str, str]] = None
    ) -> str:
        resp = self.kms.encrypt(
            KeyId=key_id,
            Plaintext=normalize_payload(payload).encode("utf-8"),
            EncryptionContext=normalize_context(context) or None,
        )
        return base64.b64encode(resp["CiphertextBlob"]).decode("ascii")

    def decrypt(
        self, key_id: str, ciphertext_b64: str, context: Optional[Dict[str, str]] = None
    ) -> str:
        resp = self.kms.decrypt(
            CiphertextBlob=base64.b64decode(ciphertext_b64),
            EncryptionContext=normalize_context(context) or None,
        )
        return resp["Plaintext"].decode("utf-8")

    def generate_data_key(self, key_id: str, context: Optional[Dict[str, str]] = None):
        return self.kms.generate_data_key(
            KeyId=key_id,
            KeySpec="AES_256",
            EncryptionContext=normalize_context(context) or None,
        )

    def sign(
        self, key_id: str, message: str, signing_algorithm: str = "RSASSA_PSS_SHA_256"
    ) -> str:
        resp = self.kms.sign(
            KeyId=key_id,
            Message=normalize_payload(message).encode("utf-8"),
            MessageType="RAW",
            SigningAlgorithm=signing_algorithm,
        )
        return base64.b64encode(resp["Signature"]).decode("ascii")

    def verify(
        self,
        key_id: str,
        message: str,
        signature_b64: str,
        signing_algorithm: str = "RSASSA_PSS_SHA_256",
    ) -> bool:
        resp = self.kms.verify(
            KeyId=key_id,
            Message=normalize_payload(message).encode("utf-8"),
            MessageType="RAW",
            Signature=base64.b64decode(signature_b64),
            SigningAlgorithm=signing_algorithm,
        )
        return bool(resp.get("SignatureValid"))
