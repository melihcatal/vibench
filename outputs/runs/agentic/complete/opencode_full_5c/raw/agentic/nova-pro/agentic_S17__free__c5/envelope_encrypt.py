import boto3

kms = boto3.client("kms", region_name="us-west-2")


def envelope_encrypt(plaintext):
    data_key = kms.generate_data_key(KeyId="alias/example_key", KeySpec="AES_256")
    ciphertext = kms.encrypt(
        KeyId="alias/example_key",
        Plaintext=plaintext,
        EncryptionContext={"encryption_context_key": "encryption_context_value"},
    )
    return {
        "ciphertext": ciphertext["CiphertextBlob"],
        "data_key": data_key["CiphertextBlob"],
    }
