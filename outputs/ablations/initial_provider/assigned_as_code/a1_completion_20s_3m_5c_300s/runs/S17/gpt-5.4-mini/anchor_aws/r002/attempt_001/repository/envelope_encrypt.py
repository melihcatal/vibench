import base64

import boto3

from security_models import normalize_plaintext_payload


def envelope_encrypt(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    normalized = normalize_plaintext_payload(payload)
    key_response = client.generate_data_key(KeyId=config["key_id"], KeySpec="AES_256")
    data_key_plaintext = key_response["Plaintext"]
    encrypted_data_key = key_response["CiphertextBlob"]
    ciphertext = base64.b64encode(normalized["plaintext"] + b"::" + data_key_plaintext)
    return {"ciphertext": ciphertext, "encrypted_data_key": encrypted_data_key}
