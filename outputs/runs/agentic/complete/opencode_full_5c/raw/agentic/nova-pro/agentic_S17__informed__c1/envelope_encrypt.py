import boto3


def envelope_encrypt(plaintext, key_id):
    client = boto3.client("kms")
    data_key = client.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    encrypted_data_key = data_key["CiphertextBlob"]
    encrypt_client = boto3.client("kms")
    encrypted_data = encrypt_client.encrypt(KeyId=key_id, Plaintext=plaintext)
    return {
        "EncryptedDataKey": encrypted_data_key,
        "CiphertextBlob": encrypted_data["CiphertextBlob"],
    }
