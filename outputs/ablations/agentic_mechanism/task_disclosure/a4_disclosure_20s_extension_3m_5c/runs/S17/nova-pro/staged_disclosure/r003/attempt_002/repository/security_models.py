from typing import Any, Dict

import boto3


def create_key(key_description: str) -> Dict[str, Any]:
    kms_client = boto3.client('kms')
    response = kms_client.create_key(Description=key_description)
    return response


def encrypt_data(key_id: str, plaintext: str) -> Dict[str, Any]:
    kms_client = boto3.client('kms')
    response = kms_client.encrypt(KeyId=key_id, Plaintext=plaintext)
    return response


def decrypt_data(ciphertext_blob: bytes) -> Dict[str, Any]:
    kms_client = boto3.client('kms')
    response = kms_client.decrypt(CiphertextBlob=ciphertext_blob)
    return response


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized_response = {}
    for key, value in response.items():
        if isinstance(value, bytes):
            normalized_response[key] = value.decode('utf-8')
        else:
            normalized_response[key] = value
    return normalized_response