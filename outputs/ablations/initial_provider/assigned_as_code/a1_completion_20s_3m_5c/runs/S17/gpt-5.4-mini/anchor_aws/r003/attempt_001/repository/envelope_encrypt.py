import boto3
import base64
import os


def envelope_encrypt(payload, config=None):
    config = config or {}
    kms = boto3.client("kms", region_name=config.get("region"))
    data_key = kms.generate_data_key(KeyId=config["key_id"], KeySpec="AES_256")
    plaintext_key = data_key["Plaintext"]
    encrypted_key = data_key["CiphertextBlob"]
    return {
        "encrypted_data_key": encrypted_key,
        "plaintext_data_key": base64.b64encode(plaintext_key).decode("utf-8"),
        "payload_length": len(payload.get("plaintext", b"")),
    }
