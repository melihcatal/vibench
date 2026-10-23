import boto3


def envelope_encrypt(plaintext):
    client = boto3.client("kms")
    data_key = client.generate_data_key(KeyId="your-key-id", KeySpec="AES_256")
    ciphertext = client.encrypt(KeyId=data_key["KeyId"], Plaintext=plaintext)
    return {
        "CiphertextBlob": ciphertext["CiphertextBlob"],
        "DataKey": data_key["CiphertextBlob"],
    }
