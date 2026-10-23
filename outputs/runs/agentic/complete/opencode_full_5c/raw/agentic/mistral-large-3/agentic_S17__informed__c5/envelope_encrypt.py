import os
from security_client import AWSKMSClient
from security_models import DataKeyRequest, normalize_data_key_response


def envelope_encrypt(key_id: str, plaintext: str) -> dict:
    """
    Implements envelope encryption using AWS KMS.

    Args:
        key_id: AWS KMS key ID or ARN.
        plaintext: Plaintext string to encrypt.

    Returns:
        Dictionary containing ciphertext, encrypted data key, and metadata.
    """
    client = AWSKMSClient()

    # Generate a data key for envelope encryption
    data_key_request = DataKeyRequest(key_id=key_id)
    data_key_response = client.generate_data_key(
        key_id=data_key_request.key_id, key_spec=data_key_request.key_spec
    )
    normalized_data_key = normalize_data_key_response(data_key_response)

    # Encrypt the plaintext with the data key (AES-256 in GCM mode)
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
    import os

    iv = os.urandom(12)
    encryptor = Cipher(
        algorithms.AES(normalized_data_key.plaintext_key),
        modes.GCM(iv),
        backend=default_backend(),
    ).encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return {
        "ciphertext": (iv + encryptor.tag + ciphertext).hex(),
        "encrypted_data_key": normalized_data_key.ciphertext_key.hex(),
        "key_id": normalized_data_key.key_id,
        "algorithm": "AES-256-GCM",
    }
