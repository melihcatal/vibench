import boto3


def envelope_encrypt(plaintext, key_id):
    client = boto3.client("kms")
    data_key = client.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    encrypted_data_key = data_key["CiphertextBlob"]
    encrypted_text = client.encrypt(KeyId=key_id, Plaintext=plaintext)["CiphertextBlob"]
    return encrypted_data_key, encrypted_text
