import boto3


def envelope_encrypt(plaintext):
    kms_client = boto3.client("kms", region_name="us-west-2")
    data_key = kms_client.generate_data_key(KeyId="alias/myKey", KeySpec="AES_256")
    ciphertext = kms_client.encrypt(KeyId=data_key["KeyId"], Plaintext=plaintext)[
        "CiphertextBlob"
    ]
    return {"Ciphertext": ciphertext, "DataKey": data_key["CiphertextBlob"]}
