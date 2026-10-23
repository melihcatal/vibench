import boto3


def envelope_encrypt(plaintext, master_key_id, data_key_length):
    kms_client = boto3.client("kms")
    response = kms_client.generate_data_key(
        KeyId=master_key_id, KeySpec=data_key_length
    )
    encrypted_data_key = response["CiphertextBlob"]
    data_key = response["Plaintext"]
    encrypted_data = boto3.client("kms").encrypt(
        KeyId=master_key_id, Plaintext=plaintext
    )["CiphertextBlob"]
    return encrypted_data_key, data_key, encrypted_data
