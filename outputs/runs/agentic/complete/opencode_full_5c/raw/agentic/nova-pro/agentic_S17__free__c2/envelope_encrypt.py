import boto3

kms = boto3.client("kms", region_name="us-west-2")


def envelope_encrypt(plaintext):
    data_key = kms.generate_data_key(KeyId="alias/myKey", KeySpec="AES_256")
    ciphertext = kms.encrypt(KeyId="alias/myKey", Plaintext=data_key["Plaintext"])[
        "CiphertextBlob"
    ]
    encrypted_data = kms.encrypt(
        KeyId="alias/myKey",
        Plaintext=plaintext,
        EncryptionContext={"aws:envelope_encryption": "true"},
    )["CiphertextBlob"]
    return ciphertext, encrypted_data
