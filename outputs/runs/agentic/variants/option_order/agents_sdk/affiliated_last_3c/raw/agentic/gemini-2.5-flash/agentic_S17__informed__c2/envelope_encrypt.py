import boto3
import os

def generate_data_key_and_encrypt(key_id: str, plaintext_data: bytes) -> tuple[bytes, bytes]:
    """
    Implements envelope encryption using AWS KMS to generate a data key and then encrypt data locally.

    Args:
        key_id: The KMS key ID or ARN to encrypt the data key.
        plaintext_data: The data to be encrypted locally.

    Returns:
        A tuple containing (encrypted_data_key, encrypted_data).
    """
    kms_client = boto3.client(
        'kms',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    # Generate a data key
    response = kms_client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256'
    )
    encrypted_data_key = response['CiphertextBlob']
    plaintext_data_key = response['Plaintext']

    # Use the plaintext data key to encrypt the data locally
    from cryptography.fernet import Fernet
    f = Fernet(plaintext_data_key)
    encrypted_data = f.encrypt(plaintext_data)

    return encrypted_data_key, encrypted_data

def decrypt_envelope_encrypted_data(encrypted_data_key: bytes, encrypted_data: bytes) -> bytes:
    """
    Decrypts data that was envelope-encrypted using AWS KMS and a local data key.

    Args:
        encrypted_data_key: The data key encrypted by KMS.
        encrypted_data: The data encrypted locally with the plaintext data key.

    Returns:
        The decrypted plaintext data.
    """
    kms_client = boto3.client(
        'kms',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    # Decrypt the data key
    response = kms_client.decrypt(
        CiphertextBlob=encrypted_data_key
    )
    plaintext_data_key = response['Plaintext']

    # Use the plaintext data key to decrypt the data locally
    from cryptography.fernet import Fernet
    f = Fernet(plaintext_data_key)
    decrypted_data = f.decrypt(encrypted_data)

    return decrypted_data
