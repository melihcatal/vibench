import os

import boto3

from security_models import encode_blob, normalize_payload, response_dict


def envelope_encrypt(payload, config=None):
    payload = normalize_payload(payload)
    config = config or {}
    region = config.get("region") or os.getenv("AWS_REGION")
    kms = boto3.client("kms", region_name=region)
    data_key = kms.generate_data_key(KeyId=config["key_id"], KeySpec="AES_256")
    plaintext = payload["plaintext"]
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")
    data_key_plaintext = data_key["Plaintext"]
    ciphertext = bytes(a ^ b for a, b in zip(plaintext, data_key_plaintext * (len(plaintext) // len(data_key_plaintext) + 1)))
    return response_dict(
        encrypted_data_key=encode_blob(data_key["CiphertextBlob"]),
        ciphertext=encode_blob(ciphertext),
    )
