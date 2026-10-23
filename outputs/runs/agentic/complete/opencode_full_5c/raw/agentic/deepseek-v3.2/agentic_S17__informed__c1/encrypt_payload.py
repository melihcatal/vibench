import base64
from typing import Dict, Any, Union
from security_client import security_client
from security_models import EncryptionRequest, EncryptionResult


def encrypt_payload(
    plaintext: Union[str, bytes, Dict[str, Any]],
    key_id: str,
    encryption_context: Dict[str, str] = None,
    algorithm: str = "SYMMETRIC_DEFAULT",
) -> Dict[str, Any]:
    """
    Encrypt a plaintext payload using AWS KMS.

    Args:
        plaintext: The data to encrypt (string, bytes, or dict)
        key_id: AWS KMS key ID or alias (e.g., 'alias/my-key', 'key-id')
        encryption_context: Optional encryption context key-value pairs
        algorithm: Encryption algorithm (default: SYMMETRIC_DEFAULT)

    Returns:
        Dict containing encrypted ciphertext and metadata
    """
    kms_client = security_client.get_kms_client()

    request = EncryptionRequest(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context,
        algorithm=algorithm,
    )

    try:
        response = kms_client.encrypt(**request.to_kms_params())

        result = EncryptionResult(
            ciphertext=response["CiphertextBlob"],
            key_id=response["KeyId"],
            encryption_context=response.get("EncryptionContext", {}),
            algorithm=response.get("EncryptionAlgorithm", algorithm),
        )

        return result.to_dict()

    except kms_client.exceptions.NotFoundException as e:
        raise ValueError(f"Key not found: {key_id}") from e
    except kms_client.exceptions.DisabledException as e:
        raise ValueError(f"Key is disabled: {key_id}") from e
    except kms_client.exceptions.KeyUnavailableException as e:
        raise ValueError(f"Key unavailable: {key_id}") from e
    except Exception as e:
        raise RuntimeError(f"Encryption failed: {str(e)}") from e


def encrypt_payload_base64(
    plaintext: Union[str, bytes, Dict[str, Any]],
    key_id: str,
    encryption_context: Dict[str, str] = None,
) -> str:
    """
    Encrypt payload and return base64-encoded ciphertext.

    Args:
        plaintext: The data to encrypt
        key_id: AWS KMS key ID or alias
        encryption_context: Optional encryption context

    Returns:
        Base64-encoded ciphertext string
    """
    result = encrypt_payload(plaintext, key_id, encryption_context)
    return result["ciphertext"]
