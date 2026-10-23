from typing import Optional, Dict, List

from security_client import get_kms_client, resolve_key_id, parse_kms_error
from security_models import (
    DecryptRequest,
    DecryptResponse,
    EncryptionAlgorithm,
    normalize_ciphertext,
    validate_key_id,
)


def decrypt_payload(
    ciphertext: bytes,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    grant_tokens: Optional[List[str]] = None,
    encryption_algorithm: Optional[EncryptionAlgorithm] = None,
) -> DecryptResponse:
    kms_client = get_kms_client()
    ciphertext_blob = normalize_ciphertext(ciphertext)

    decrypt_params = {
        "CiphertextBlob": ciphertext_blob,
    }

    if key_id:
        decrypt_params["KeyId"] = resolve_key_id(validate_key_id(key_id))
    if encryption_context:
        decrypt_params["EncryptionContext"] = encryption_context
    if grant_tokens:
        decrypt_params["GrantTokens"] = grant_tokens
    if encryption_algorithm:
        decrypt_params["EncryptionAlgorithm"] = encryption_algorithm.value

    request = DecryptRequest(
        ciphertext_blob=ciphertext_blob,
        encryption_context=encryption_context,
        grant_tokens=grant_tokens,
        encryption_algorithm=encryption_algorithm,
    )

    try:
        response = kms_client.decrypt(**decrypt_params)
        return DecryptResponse(
            plaintext=response["Plaintext"],
            key_id=response["KeyId"],
            encryption_algorithm=response["EncryptionAlgorithm"],
            request_id=response["ResponseMetadata"]["RequestId"],
            http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
        )
    except Exception as e:
        error_info = parse_kms_error(e)
        raise RuntimeError(
            f"AWS KMS Decrypt failed: "
            f"[{error_info['error_code']}] {error_info['error_message']}"
        ) from e


def decrypt_and_decode(
    ciphertext_b64: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> str:
    response = decrypt_payload(
        ciphertext=ciphertext_b64,
        key_id=key_id,
        encryption_context=encryption_context,
    )
    return response.plaintext.decode("utf-8")
