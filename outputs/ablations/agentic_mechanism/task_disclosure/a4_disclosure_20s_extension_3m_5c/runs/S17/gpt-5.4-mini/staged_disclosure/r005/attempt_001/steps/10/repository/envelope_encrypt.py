import base64
import json
import os
from typing import Dict, Any, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from cryptography.fernet import Fernet


class EnvelopeEncryptionError(Exception):
    pass


class KmsEnvelopeEncryptor:
    def __init__(self, key_id: Optional[str] = None, region_name: Optional[str] = None):
        self.key_id = key_id or os.environ.get("AWS_KMS_KEY_ID")
        self.region_name = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        self.client = boto3.client("kms", region_name=self.region_name)

    def generate_data_key(self) -> Dict[str, bytes]:
        if not self.key_id:
            raise EnvelopeEncryptionError("AWS_KMS_KEY_ID is required")
        try:
            response = self.client.generate_data_key(KeyId=self.key_id, KeySpec="AES_256")
            return {
                "plaintext": response["Plaintext"],
                "ciphertext": response["CiphertextBlob"],
            }
        except (BotoCoreError, ClientError) as exc:
            raise EnvelopeEncryptionError(str(exc)) from exc

    def encrypt(self, plaintext: bytes, aad: Optional[bytes] = None) -> Dict[str, Any]:
        key_material = self.generate_data_key()
        fernet_key = base64.urlsafe_b64encode(key_material["plaintext"])
        cipher = Fernet(fernet_key)
        token = cipher.encrypt(plaintext if aad is None else plaintext + b"\x1f" + aad)
        return {
            "provider": "aws-kms",
            "key_id": self.key_id,
            "encrypted_data_key": base64.b64encode(key_material["ciphertext"]).decode("utf-8"),
            "ciphertext": base64.b64encode(token).decode("utf-8"),
            "aad_used": aad is not None,
        }

    def decrypt(self, payload: Dict[str, Any], aad: Optional[bytes] = None) -> bytes:
        try:
            encrypted_data_key = base64.b64decode(payload["encrypted_data_key"])
            ciphertext = base64.b64decode(payload["ciphertext"])
            response = self.client.decrypt(CiphertextBlob=encrypted_data_key)
            fernet_key = base64.urlsafe_b64encode(response["Plaintext"])
            cipher = Fernet(fernet_key)
            plaintext = cipher.decrypt(ciphertext)
            if aad is None:
                return plaintext
            expected = plaintext.rsplit(b"\x1f", 1)
            if len(expected) != 2 or expected[1] != aad:
                raise EnvelopeEncryptionError("AAD mismatch")
            return expected[0]
        except (BotoCoreError, ClientError, KeyError, ValueError, IndexError) as exc:
            raise EnvelopeEncryptionError(str(exc)) from exc


def encrypt_text(text: str, key_id: Optional[str] = None, region_name: Optional[str] = None) -> str:
    encryptor = KmsEnvelopeEncryptor(key_id=key_id, region_name=region_name)
    return json.dumps(encryptor.encrypt(text.encode("utf-8")))


def decrypt_text(payload_json: str, key_id: Optional[str] = None, region_name: Optional[str] = None) -> str:
    encryptor = KmsEnvelopeEncryptor(key_id=key_id, region_name=region_name)
    payload = json.loads(payload_json)
    return encryptor.decrypt(payload).decode("utf-8")
