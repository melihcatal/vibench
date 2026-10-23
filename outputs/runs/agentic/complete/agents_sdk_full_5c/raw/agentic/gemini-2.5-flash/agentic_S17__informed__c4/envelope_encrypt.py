import boto3
import os

def envelope_encrypt(key_id: str, plaintext: bytes) -> tuple[bytes, bytes]:
    """
    Implements envelope encryption using AWS KMS to generate a data key
    and encrypts the plaintext locally.
    """
    kms_client = boto3.client(
        "kms",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    # Generate a data key
    generate_key_response = kms_client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256'
    )

    data_key_plaintext = generate_key_response['Plaintext']
    data_key_ciphertext_blob = generate_key_response['CiphertextBlob']

    # Use the data key to encrypt the payload locally
    # For simplicity, we'll use a basic XOR encryption here. In a real-world scenario,
    # you'd use a robust symmetric encryption library like cryptography.io
    encrypted_payload_local = bytes([p ^ k for p, k in zip(plaintext, data_key_plaintext * (len(plaintext) // len(data_key_plaintext) + 1))])

    return data_key_ciphertext_blob, encrypted_payload_local

