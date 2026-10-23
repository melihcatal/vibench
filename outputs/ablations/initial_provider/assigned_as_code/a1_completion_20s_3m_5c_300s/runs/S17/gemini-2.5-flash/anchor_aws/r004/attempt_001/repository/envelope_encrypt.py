import boto3
from cryptography.fernet import Fernet


def envelope_encrypt(payload, config=None):
    config = config or {}
    kms_client = boto3.client("kms", region_name=config.get("region"))

    # Generate a data key
    response = kms_client.generate_data_key(KeyId=config["key_id"], KeySpec="AES_256")
    plaintext_data_key = response["Plaintext"]
    encrypted_data_key = response["CiphertextBlob"]

    # Encrypt the actual payload locally with the plaintext data key
    f = Fernet(plaintext_data_key)
    local_ciphertext = f.encrypt(payload["plaintext"])

    return {
        "ciphertext": local_ciphertext,
        "encrypted_data_key": encrypted_data_key,
    }


def envelope_decrypt(payload, config=None):
    config = config or {}
    kms_client = boto3.client("kms", region_name=config.get("region"))

    # Decrypt the encrypted data key using KMS
    response = kms_client.decrypt(CiphertextBlob=payload["encrypted_data_key"])
    plaintext_data_key = response["Plaintext"]

    # Decrypt the actual payload locally with the plaintext data key
    f = Fernet(plaintext_data_key)
    local_plaintext = f.decrypt(payload["ciphertext"])

    return {"plaintext": local_plaintext}
