import base64
from typing import Dict, Any, Union
from security_client import security_client
from security_models import (
    SignatureRequest,
    SignatureResult,
    VerificationRequest,
    VerificationResult,
)


def sign_message(
    message: Union[str, bytes, Dict[str, Any]],
    key_id: str,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    message_type: str = "RAW",
) -> Dict[str, Any]:
    """
    Sign a message using AWS KMS.

    Args:
        message: The message to sign
        key_id: AWS KMS key ID or alias
        signing_algorithm: Signing algorithm (default: RSASSA_PSS_SHA_256)
        message_type: Message type (RAW or DIGEST)

    Returns:
        Dict containing signature and metadata
    """
    kms_client = security_client.get_kms_client()

    request = SignatureRequest(
        message=message,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        message_type=message_type,
    )

    try:
        response = kms_client.sign(**request.to_kms_params())

        result = SignatureResult(
            signature=response["Signature"],
            key_id=response["KeyId"],
            signing_algorithm=response["SigningAlgorithm"],
            message_type=response.get("MessageType", message_type),
        )

        return result.to_dict()

    except kms_client.exceptions.NotFoundException as e:
        raise ValueError(f"Key not found: {key_id}") from e
    except kms_client.exceptions.DisabledException as e:
        raise ValueError(f"Key is disabled: {key_id}") from e
    except kms_client.exceptions.KeyUnavailableException as e:
        raise ValueError(f"Key unavailable: {key_id}") from e
    except kms_client.exceptions.InvalidKeyUsageException as e:
        raise ValueError(f"Key cannot be used for signing") from e
    except Exception as e:
        raise RuntimeError(f"Signing failed: {str(e)}") from e


def verify_signature(
    message: Union[str, bytes, Dict[str, Any]],
    signature: Union[str, bytes],
    key_id: str,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    message_type: str = "RAW",
) -> Dict[str, Any]:
    """
    Verify a signature using AWS KMS.

    Args:
        message: The original message
        signature: The signature to verify
        key_id: AWS KMS key ID or alias
        signing_algorithm: Signing algorithm (default: RSASSA_PSS_SHA_256)
        message_type: Message type (RAW or DIGEST)

    Returns:
        Dict containing verification result
    """
    kms_client = security_client.get_kms_client()

    request = VerificationRequest(
        message=message,
        signature=signature,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        message_type=message_type,
    )

    try:
        response = kms_client.verify(**request.to_kms_params())

        result = VerificationResult(
            is_valid=response["SignatureValid"],
            key_id=response["KeyId"],
            signing_algorithm=response["SigningAlgorithm"],
        )

        return result.to_dict()

    except kms_client.exceptions.NotFoundException as e:
        raise ValueError(f"Key not found: {key_id}") from e
    except kms_client.exceptions.DisabledException as e:
        raise ValueError(f"Key is disabled: {key_id}") from e
    except kms_client.exceptions.KeyUnavailableException as e:
        raise ValueError(f"Key unavailable: {key_id}") from e
    except kms_client.exceptions.InvalidKeyUsageException as e:
        raise ValueError(f"Key cannot be used for verification") from e
    except kms_client.exceptions.InvalidSignatureException as e:
        result = VerificationResult(
            is_valid=False, key_id=key_id, signing_algorithm=signing_algorithm
        )
        return result.to_dict()
    except Exception as e:
        raise RuntimeError(f"Verification failed: {str(e)}") from e


def sign_message_base64(message: Union[str, bytes, Dict[str, Any]], key_id: str) -> str:
    """
    Sign message and return base64-encoded signature.

    Args:
        message: The message to sign
        key_id: AWS KMS key ID or alias

    Returns:
        Base64-encoded signature string
    """
    result = sign_message(message, key_id)
    return result["signature"]


def verify_signature_base64(
    message: Union[str, bytes, Dict[str, Any]], signature: str, key_id: str
) -> bool:
    """
    Verify a base64-encoded signature.

    Args:
        message: The original message
        signature: Base64-encoded signature
        key_id: AWS KMS key ID or alias

    Returns:
        True if signature is valid, False otherwise
    """
    result = verify_signature(message, signature, key_id)
    return result["is_valid"]
