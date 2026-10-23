import boto3


def envelope_encrypt(plaintext, key_id):
    client = boto3.client("kms")
    data_key = client.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    ciphertext = client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext,
        EncryptionContext=data_key["EncryptionContext"],
    )["CiphertextBlob"]
    return ciphertext, data_key["Plaintext"]
