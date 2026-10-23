import base64
import os
from typing import Any, Dict

import boto3

from security_models import normalize_bytes, normalize_text


def get_kms_client():
    return boto3.client('kms')


def get_transcribe_client():
    return boto3.client('translate')


def load_config() -> Dict[str, Any]:
    return {
        'kms_key_id': os.getenv('AWS_KMS_KEY_ID', ''),
        'region': os.getenv('AWS_REGION', os.getenv('AWS_DEFAULT_REGION', 'us-east-1')),
    }


def encrypt_with_kms(key_id: str, plaintext: Any) -> str:
    client = get_kms_client()
    result = client.encrypt(KeyId=key_id, Plaintext=normalize_bytes(plaintext))
    return base64.b64encode(result['CiphertextBlob']).decode('utf-8')


def decrypt_with_kms(key_id: str, ciphertext: Any) -> str:
    client = get_kms_client()
    blob = base64.b64decode(normalize_text(ciphertext).encode('utf-8'))
    result = client.decrypt(KeyId=key_id, CiphertextBlob=blob)
    return result['Plaintext'].decode('utf-8')


def sign_with_kms(key_id: str, message: Any, algorithm: str = 'RSASSA_PSS_SHA_256') -> str:
    client = get_kms_client()
    result = client.sign(KeyId=key_id, Message=normalize_bytes(message), MessageType='RAW', SigningAlgorithm=algorithm)
    return base64.b64encode(result['Signature']).decode('utf-8')


def verify_with_kms(key_id: str, message: Any, signature: Any, algorithm: str = 'RSASSA_PSS_SHA_256') -> bool:
    client = get_kms_client()
    result = client.verify(
        KeyId=key_id,
        Message=normalize_bytes(message),
        MessageType='RAW',
        Signature=base64.b64decode(normalize_text(signature).encode('utf-8')),
        SigningAlgorithm=algorithm,
    )
    return bool(result['SignatureValid'])
