from typing import Optional, Dict, List

from security_client import get_kms_client, resolve_key_id, parse_kms_error
from security_models import (
    EncryptRequest,
    EncryptResponse,
    EncryptionAlgorithm,
    normalize_plaintext,
    validate_plaintext,
    validate_key_id,
    encode_ciphertext,
)


def encrypt_payload(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT,
    grant_tokens: Optional[List[str]] = None,
) -> EncryptResponse:
    kms_client = get_kms_client()
    resolved_key_id = resolve_key_id(validate_key_id(key_id))
    plaintext_bytes = validate_plaintext(normalize_plaintext(plaintext))

    encrypt_params = {
        "KeyId": resolved_key_id,
        "Plaintext": plaintext_bytes,
        "EncryptionAlgorithm": encryption_algorithm.value,
    }

    if encryption_context:
        encrypt_params["EncryptionContext"] = encryption_context
    if grant_tokens:
        encrypt_params["GrantTokens"] = grant_tokens

    request = EncryptRequest(
        key_id=resolved_key_id,
        plaintext=plaintext_bytes,
        encryption_context=encryption_context,
        encryption_algorithm=encryption_algorithm,
        grant_tokens=grant_tokens,
    )

    try:
        response = kms_client.encrypt(**encrypt_params)
        return EncryptResponse(
            ciphertext_blob=response["CiphertextBlob"],
            key_id=response["KeyId"],
            encryption_algorithm=response["EncryptionAlgorithm"],
            request_id=response["ResponseMetadata"]["RequestId"],
            http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
        )
    except Exception as e:
        error_info = parse_kms_error(e)
        raise RuntimeError(
            f"AWS KMS Encrypt failed for key {resolved_key_id}: "
            f"[{error_info['error_code']}] {error_info['error_message']}"
        ) from e


def encrypt_and_encode(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    response = encrypt_payload(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context,
    )
    return {
        "ciphertext": encode_ciphertext(response.ciphertext_blob),
        "key_id": response.key_id,
        "encryption_algorithm": response.encryption_algorithm,
        "request_id": response.request_id,
    }
