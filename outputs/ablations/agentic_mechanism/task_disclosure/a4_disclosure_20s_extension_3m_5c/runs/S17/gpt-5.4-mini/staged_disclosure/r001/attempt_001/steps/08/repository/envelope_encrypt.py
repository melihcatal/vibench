import base64
import json
import os
from dataclasses import dataclass

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from cryptography.fernet import Fernet


@dataclass
class EnvelopeCiphertext:
    key_id: str
    encrypted_data_key: str
    nonce: str
    ciphertext: str

    def to_json(self) -> str:
        return json.dumps({
            "key_id": self.key_id,
            "encrypted_data_key": self.encrypted_data_key,
            "nonce": self.nonce,
            "ciphertext": self.ciphertext,
        })

    @staticmethod
    def from_json(payload: str) -> "EnvelopeCiphertext":
        obj = json.loads(payload)
        return EnvelopeCiphertext(
            key_id=obj["key_id"],
            encrypted_data_key=obj["encrypted_data_key"],
            nonce=obj["nonce"],
            ciphertext=obj["ciphertext"],
        )


class KmsEnvelopeEncryption:
    def __init__(self, kms_key_id: str, region_name: str | None = None):
        self.kms_key_id = kms_key_id
        self.kms = boto3.client("kms", region_name=region_name or os.getenv("AWS_REGION"))

    def encrypt(self, plaintext: bytes) -> str:
        try:
            data_key_resp = self.kms.generate_data_key(KeyId=self.kms_key_id, KeySpec="AES_256")
            plaintext_data_key = data_key_resp["Plaintext"]
            encrypted_data_key = data_key_resp["CiphertextBlob"]
            fernet_key = base64.urlsafe_b64encode(plaintext_data_key)
            fernet = Fernet(fernet_key)
            ciphertext = fernet.encrypt(plaintext)
            payload = EnvelopeCiphertext(
                key_id=self.kms_key_id,
                encrypted_data_key=base64.b64encode(encrypted_data_key).decode("utf-8"),
                nonce="",
                ciphertext=ciphertext.decode("utf-8"),
            )
            return payload.to_json()
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f"AWS KMS envelope encryption failed: {exc}") from exc

    def decrypt(self, payload_json: str) -> bytes:
        try:
            payload = EnvelopeCiphertext.from_json(payload_json)
            encrypted_data_key = base64.b64decode(payload.encrypted_data_key)
            data_key_resp = self.kms.decrypt(CiphertextBlob=encrypted_data_key)
            plaintext_data_key = data_key_resp["Plaintext"]
            fernet_key = base64.urlsafe_b64encode(plaintext_data_key)
            fernet = Fernet(fernet_key)
            return fernet.decrypt(payload.ciphertext.encode("utf-8"))
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f"AWS KMS envelope decryption failed: {exc}") from exc


def encrypt_text(plaintext: str, kms_key_id: str, region_name: str | None = None) -> str:
    return KmsEnvelopeEncryption(kms_key_id, region_name).encrypt(plaintext.encode("utf-8"))


def decrypt_text(payload_json: str, kms_key_id: str, region_name: str | None = None) -> str:
    return KmsEnvelopeEncryption(kms_key_id, region_name).decrypt(payload_json).decode("utf-8")
