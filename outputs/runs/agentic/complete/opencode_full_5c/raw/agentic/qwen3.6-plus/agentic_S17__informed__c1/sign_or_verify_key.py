import os
import base64
from security_client import (
    AWSSecurityClient,
    normalize_plaintext,
    encode_bytes_to_base64,
    decode_base64_to_bytes,
)
from security_models import (
    SignVerifyRequest,
    SigningAlgorithm,
    MessageType,
    load_kms_config,
)


def sign_or_verify(
    key_id: str,
    message: str = None,
    signature_b64: str = None,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    operation: str = "sign",
) -> dict:
    config = load_kms_config()
    client = AWSSecurityClient(config)

    algorithm = SigningAlgorithm(signing_algorithm)

    if operation == "sign":
        message_bytes = normalize_plaintext(message)
        request = SignVerifyRequest(
            key_id=key_id,
            message=message_bytes,
            signing_algorithm=algorithm,
            message_type=MessageType.RAW,
        )
        response = client.sign(request)
        return {
            "operation": "sign",
            "signature": encode_bytes_to_base64(response.signature),
            "key_id": response.key_id,
            "signing_algorithm": response.signing_algorithm,
            "request_id": response.request_id,
        }
    elif operation == "verify":
        message_bytes = normalize_plaintext(message)
        signature_bytes = decode_base64_to_bytes(signature_b64)
        request = SignVerifyRequest(
            key_id=key_id,
            message=message_bytes,
            signature=signature_bytes,
            signing_algorithm=algorithm,
            message_type=MessageType.RAW,
        )
        response = client.verify(request)
        return {
            "operation": "verify",
            "signature_valid": response.signature_valid,
            "key_id": response.key_id,
            "signing_algorithm": response.signing_algorithm,
            "request_id": response.request_id,
        }
    else:
        raise ValueError(f"Unsupported operation: {operation}. Use 'sign' or 'verify'.")


if __name__ == "__main__":
    key_id = os.environ.get("AWS_KMS_KEY_ID", "")
    message = os.environ.get("SIGN_MESSAGE", "message-to-sign")
    operation = os.environ.get("SIGN_OPERATION", "sign")
    signature = os.environ.get("SIGN_SIGNATURE_B64", "")
    result = sign_or_verify(key_id, message, signature, operation=operation)
    print(result)
