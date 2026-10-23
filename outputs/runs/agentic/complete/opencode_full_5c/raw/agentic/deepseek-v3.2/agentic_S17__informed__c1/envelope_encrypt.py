import os
import base64
from typing import Dict, Any, Union, Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from security_client import security_client
from security_models import (
    EncryptionRequest,
    EncryptionResult,
    DecryptionRequest,
    DecryptionResult,
)


def generate_data_key(
    key_id: str, encryption_context: Dict[str, str] = None
) -> Tuple[bytes, bytes]:
    """
    Generate a data key using AWS KMS.

    Args:
        key_id: AWS KMS key ID or alias
        encryption_context: Optional encryption context

    Returns:
        Tuple of (plaintext_data_key, encrypted_data_key)
    """
    kms_client = security_client.get_kms_client()

    try:
        response = kms_client.generate_data_key(
            KeyId=key_id, KeySpec="AES_256", EncryptionContext=encryption_context or {}
        )

        return response["Plaintext"], response["CiphertextBlob"]

    except Exception as e:
        raise RuntimeError(f"Failed to generate data key: {str(e)}") from e


def encrypt_with_data_key(plaintext: bytes, data_key: bytes) -> bytes:
    """
    Encrypt data using a locally generated AES-256 data key.

    Args:
        plaintext: Data to encrypt
        data_key: AES-256 key (32 bytes)

    Returns:
        Encrypted ciphertext
    """
    if len(data_key) != 32:
        raise ValueError(f"Data key must be 32 bytes, got {len(data_key)} bytes")

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(data_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return iv + ciphertext


def decrypt_with_data_key(ciphertext: bytes, data_key: bytes) -> bytes:
    """
    Decrypt data using a locally generated AES-256 data key.

    Args:
        ciphertext: Data to decrypt (IV + ciphertext)
        data_key: AES-256 key (32 bytes)

    Returns:
        Decrypted plaintext
    """
    if len(data_key) != 32:
        raise ValueError(f"Data key must be 32 bytes, got {len(data_key)} bytes")

    if len(ciphertext) < 16:
        raise ValueError("Ciphertext too short to contain IV")

    iv = ciphertext[:16]
    encrypted_data = ciphertext[16:]

    cipher = Cipher(algorithms.AES(data_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext


def envelope_encrypt(
    plaintext: Union[str, bytes, Dict[str, Any]],
    key_id: str,
    encryption_context: Dict[str, str] = None,
) -> Dict[str, Any]:
    """
    Implement envelope encryption using AWS KMS.

    Args:
        plaintext: Data to encrypt
        key_id: AWS KMS key ID or alias
        encryption_context: Optional encryption context

    Returns:
        Dict containing encrypted data key and encrypted data
    """
    from security_client import security_client

    normalized_plaintext = security_client.normalize_payload(plaintext)

    data_key_plaintext, data_key_encrypted = generate_data_key(
        key_id, encryption_context
    )

    encrypted_data = encrypt_with_data_key(normalized_plaintext, data_key_plaintext)

    return {
        "encrypted_data_key": base64.b64encode(data_key_encrypted).decode("utf-8"),
        "encrypted_data": base64.b64encode(encrypted_data).decode("utf-8"),
        "key_id": key_id,
        "encryption_context": encryption_context or {},
    }


def envelope_decrypt(
    encrypted_data_key: Union[str, bytes],
    encrypted_data: Union[str, bytes],
    encryption_context: Dict[str, str] = None,
) -> bytes:
    """
    Decrypt envelope-encrypted data using AWS KMS.

    Args:
        encrypted_data_key: Encrypted data key from KMS
        encrypted_data: Locally encrypted data
        encryption_context: Optional encryption context

    Returns:
        Decrypted plaintext
    """
    kms_client = security_client.get_kms_client()

    if isinstance(encrypted_data_key, str):
        encrypted_data_key = base64.b64decode(encrypted_data_key)

    if isinstance(encrypted_data, str):
        encrypted_data = base64.b64decode(encrypted_data)

    try:
        response = kms_client.decrypt(
            CiphertextBlob=encrypted_data_key,
            EncryptionContext=encryption_context or {},
        )

        data_key_plaintext = response["Plaintext"]

        plaintext = decrypt_with_data_key(encrypted_data, data_key_plaintext)

        return plaintext

    except kms_client.exceptions.IncorrectKeyException as e:
        raise ValueError(f"Incorrect key for decryption") from e
    except kms_client.exceptions.InvalidCiphertextException as e:
        raise ValueError(f"Invalid ciphertext") from e
    except Exception as e:
        raise RuntimeError(f"Envelope decryption failed: {str(e)}") from e
