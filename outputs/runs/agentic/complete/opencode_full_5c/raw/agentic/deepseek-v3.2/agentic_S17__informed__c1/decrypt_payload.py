import base64
from typing import Dict, Any, Union
from security_client import security_client
from security_models import DecryptionRequest, DecryptionResult


def decrypt_payload(
    ciphertext: Union[str, bytes],
    key_id: str = None,
    encryption_context: Dict[str, str] = None,
    algorithm: str = "SYMMETRIC_DEFAULT",
) -> Dict[str, Any]:
    """
    Decrypt a ciphertext payload using AWS KMS.

    Args:
        ciphertext: The encrypted data (base64 string or bytes)
        key_id: Optional AWS KMS key ID (can be inferred from ciphertext)
        encryption_context: Optional encryption context key-value pairs
        algorithm: Encryption algorithm (default: SYMMETRIC_DEFAULT)

    Returns:
        Dict containing decrypted plaintext and metadata
    """
    kms_client = security_client.get_kms_client()

    request = DecryptionRequest(
        ciphertext=ciphertext,
        key_id=key_id,
        encryption_context=encryption_context,
        algorithm=algorithm,
    )

    try:
        response = kms_client.decrypt(**request.to_kms_params())

        result = DecryptionResult(
            plaintext=response["Plaintext"],
            key_id=response["KeyId"],
            encryption_context=response.get("EncryptionContext", {}),
            algorithm=response.get("EncryptionAlgorithm", algorithm),
        )

        return result.to_dict()

    except kms_client.exceptions.IncorrectKeyException as e:
        raise ValueError(f"Incorrect key for decryption") from e
    except kms_client.exceptions.InvalidCiphertextException as e:
        raise ValueError(f"Invalid ciphertext") from e
    except kms_client.exceptions.KeyUnavailableException as e:
        raise ValueError(f"Key unavailable") from e
    except Exception as e:
        raise RuntimeError(f"Decryption failed: {str(e)}") from e


def decrypt_payload_to_string(
    ciphertext: Union[str, bytes],
    key_id: str = None,
    encryption_context: Dict[str, str] = None,
) -> str:
    """
    Decrypt payload and return as string.

    Args:
        ciphertext: The encrypted data
        key_id: Optional AWS KMS key ID
        encryption_context: Optional encryption context

    Returns:
        Decrypted plaintext as string
    """
    result = decrypt_payload(ciphertext, key_id, encryption_context)
    return result["plaintext"]


def decrypt_payload_to_dict(
    ciphertext: Union[str, bytes],
    key_id: str = None,
    encryption_context: Dict[str, str] = None,
) -> Dict[str, Any]:
    """
    Decrypt payload and parse as JSON dict.

    Args:
        ciphertext: The encrypted data
        key_id: Optional AWS KMS key ID
        encryption_context: Optional encryption context

    Returns:
        Decrypted and parsed JSON data as dict
    """
    import json

    result = decrypt_payload(ciphertext, key_id, encryption_context)
    return json.loads(result["plaintext"])
