import boto3
from botocore.exceptions import ClientError


def envelope_encrypt(plaintext):
    client = boto3.client("kms")
    try:
        data_key = client.generate_data_key(
            KeyId="alias/example_key", KeySpec="AES_256"
        )
        ciphertext = client.encrypt(KeyId=data_key["KeyId"], Plaintext=plaintext)[
            "CiphertextBlob"
        ]
        return {
            "CiphertextBlob": ciphertext,
            "KeyCiphertext": data_key["CiphertextBlob"],
        }
    except ClientError as e:
        print(e)
        return None
