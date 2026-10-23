import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


@dataclass
class EnvelopeCiphertext:
    encrypted_data_key: str
    nonce: str
    ciphertext: str
    kms_key_id: str


class EnvelopeEncryptionError(Exception):
    pass


class KmsEnvelopeEncryptor:
    def __init__(self, kms_key_id: str, region_name: Optional[str] = None) -> None:
        self.kms_key_id = kms_key_id
        self.kms_client = boto3.client("kms", region_name=region_name or os.getenv("AWS_REGION"))

    def encrypt(self, plaintext: bytes, encryption_context: Optional[Dict[str, str]] = None) -> EnvelopeCiphertext:
        try:
            data_key_resp = self.kms_client.generate_data_key(
                KeyId=self.kms_key_id,
                KeySpec="AES_256",
                EncryptionContext=encryption_context or {},
            )
            plaintext_key = data_key_resp["Plaintext"]
            encrypted_key = data_key_resp["CiphertextBlob"]
            aesgcm = AESGCM(plaintext_key)
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, plaintext, None)
            return EnvelopeCiphertext(
                encrypted_data_key=base64.b64encode(encrypted_key).decode("utf-8"),
                nonce=base64.b64encode(nonce).decode("utf-8"),
                ciphertext=base64.b64encode(ciphertext).decode("utf-8"),
                kms_key_id=self.kms_key_id,
            )
        except (BotoCoreError, ClientError) as exc:
            raise EnvelopeEncryptionError(str(exc)) from exc

    def decrypt(self, envelope: EnvelopeCiphertext, encryption_context: Optional[Dict[str, str]] = None) -> bytes:
        try:
            encrypted_key = base64.b64decode(envelope.encrypted_data_key)
            nonce = base64.b64decode(envelope.nonce)
            ciphertext = base64.b64decode(envelope.ciphertext)
            data_key_resp = self.kms_client.decrypt(
                CiphertextBlob=encrypted_key,
                EncryptionContext=encryption_context or {},
            )
            plaintext_key = data_key_resp["Plaintext"]
            aesgcm = AESGCM(plaintext_key)
            return aesgcm.decrypt(nonce, ciphertext, None)
        except (BotoCoreError, ClientError, ValueError) as exc:
            raise EnvelopeEncryptionError(str(exc)) from exc


def encrypt_text(text: str, kms_key_id: str, region_name: Optional[str] = None) -> str:
    encryptor = KmsEnvelopeEncryptor(kms_key_id=kms_key_id, region_name=region_name)
    envelope = encryptor.encrypt(text.encode("utf-8"))
    return json.dumps(envelope.__dict__)


def decrypt_text(envelope_json: str, kms_key_id: str, region_name: Optional[str] = None) -> str:
    encryptor = KmsEnvelopeEncryptor(kms_key_id=kms_key_id, region_name=region_name)
    envelope_data: Dict[str, Any] = json.loads(envelope_json)
    envelope = EnvelopeCiphertext(**envelope_data)
    return encryptor.decrypt(envelope).decode("utf-8")
