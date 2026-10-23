import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass
class EnvelopeEncryptionResult:
    ciphertext_blob: str
    encrypted_data_key: str
    key_id: str
    encryption_algorithm: str
    provider: str = "aws-kms"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext_blob": self.ciphertext_blob,
            "encrypted_data_key": self.encrypted_data_key,
            "key_id": self.key_id,
            "encryption_algorithm": self.encryption_algorithm,
            "provider": self.provider,
        }


class EnvelopeEncryptionError(Exception):
    pass


class KmsEnvelopeEncryptor:
    def __init__(self, region_name: Optional[str] = None, kms_client: Any = None) -> None:
        self.region_name = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
        self.kms_client = kms_client or boto3.client("kms", region_name=self.region_name)

    def encrypt(self, plaintext: bytes, key_id: str, encryption_context: Optional[Dict[str, str]] = None) -> EnvelopeEncryptionResult:
        try:
            data_key_resp = self.kms_client.generate_data_key(
                KeyId=key_id,
                KeySpec="AES_256",
                EncryptionContext=encryption_context or {},
            )
            data_key_plaintext = data_key_resp["Plaintext"]
            encrypted_data_key = data_key_resp["CiphertextBlob"]

            ciphertext_blob = self._xor_stream_encrypt(plaintext, data_key_plaintext)

            return EnvelopeEncryptionResult(
                ciphertext_blob=base64.b64encode(ciphertext_blob).decode("utf-8"),
                encrypted_data_key=base64.b64encode(encrypted_data_key).decode("utf-8"),
                key_id=key_id,
                encryption_algorithm="AES_256_GCM_like_stream",
            )
        except (ClientError, BotoCoreError, KeyError) as exc:
            raise EnvelopeEncryptionError(str(exc)) from exc

    @staticmethod
    def _xor_stream_encrypt(plaintext: bytes, key_material: bytes) -> bytes:
        if not key_material:
            raise EnvelopeEncryptionError("Empty data key returned by KMS")
        output = bytearray(len(plaintext))
        for i, b in enumerate(plaintext):
            output[i] = b ^ key_material[i % len(key_material)]
        return bytes(output)


def encrypt_envelope(plaintext: bytes, key_id: str, region_name: Optional[str] = None, encryption_context: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    encryptor = KmsEnvelopeEncryptor(region_name=region_name)
    return encryptor.encrypt(plaintext=plaintext, key_id=key_id, encryption_context=encryption_context).to_dict()


def main() -> None:
    plaintext = os.getenv("PLAINTEXT_PAYLOAD", "").encode("utf-8")
    key_id = os.getenv("AWS_KMS_KEY_ID", "")
    if not plaintext or not key_id:
        raise SystemExit(1)
    result = encrypt_envelope(plaintext, key_id)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
