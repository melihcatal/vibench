import boto3

kms = boto3.client("kms", region_name="us-west-2")


def envelope_encrypt(plaintext):
    data_key = kms.generate_data_key(KeyId="alias/example_key", KeySpec="AES_256")
    ciphertext = kms.encrypt(
        KeyId="alias/example_key", Plaintext=data_key["Plaintext"]
    )["CiphertextBlob"]
    encrypted_data_key = data_key["CiphertextBlob"]
    return ciphertext, encrypted_data_key
