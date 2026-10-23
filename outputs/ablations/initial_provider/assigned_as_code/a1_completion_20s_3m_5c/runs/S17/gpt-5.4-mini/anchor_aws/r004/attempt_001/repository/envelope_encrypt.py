import base64
import boto3


def envelope_encrypt(payload, config=None):
    config = config or {}
    kms = boto3.client("kms", region_name=config.get("region"))
    data_key = kms.generate_data_key(KeyId=config["key_id"], KeySpec="AES_256")
    plaintext_key = data_key["Plaintext"]
    encrypted_key = data_key["CiphertextBlob"]
    ciphertext = base64.b64encode(payload["plaintext"] + plaintext_key)
    return {"encrypted_data_key": encrypted_key, "ciphertext": ciphertext}
