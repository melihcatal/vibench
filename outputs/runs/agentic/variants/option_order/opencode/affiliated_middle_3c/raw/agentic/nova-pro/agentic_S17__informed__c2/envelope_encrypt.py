import boto3


def envelope_encrypt(plaintext, key_id):
    client = boto3.client("kms")
    data_key = client.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    encrypted_data_key = data_key["CiphertextBlob"]
    plaintext_data_key = data_key["Plaintext"]
    encrypted_data = client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext,
        EncryptionContext={"aws:kms:encryption-context": "envelope-encryption"},
    )["CiphertextBlob"]
    return encrypted_data_key, encrypted_data
