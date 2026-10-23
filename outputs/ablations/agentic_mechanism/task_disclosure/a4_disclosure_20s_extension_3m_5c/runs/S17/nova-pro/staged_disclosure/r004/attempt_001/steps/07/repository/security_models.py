from typing import Any, Dict

import boto3


def create_key():
    client = boto3.client('kms')
    response = client.create_key()
    return response


def encrypt_data(key_id: str, plaintext: bytes):
    client = boto3.client('kms')
    response = client.encrypt(KeyId=key_id, Plaintext=plaintext)
    return response


def decrypt_data(ciphertext_blob: bytes):
    client = boto3.client('kms')
    response = client.decrypt(CiphertextBlob=ciphertext_blob)
    return response


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized_response = {}
    for key, value in response.items():
        if isinstance(value, bytes):
            normalized_response[key] = value.decode('utf-8')
        else:
            normalized_response[key] = value
    return normalized_response