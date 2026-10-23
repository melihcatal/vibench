import os
from security_client import get_aws_kms_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_with_kms(request: DecryptionRequest) -> DecryptionResponse:
    """
    Decrypts a ciphertext payload using the corresponding AWS KMS key.
    """
    kms_client = get_aws_kms_client()
    key_id = request.key_id or os.environ.get("AWS_KMS_KEY_ID")

    if not key_id:
         return DecryptionResponse(
            plaintext=b"",
            key_id="",
            success=False,
            error="No key ID provided for decryption.",
        )

    try:
        response = kms_client.decrypt(
            KeyId=key_id,
            CiphertextBlob=request.ciphertext,
            EncryptionContext=request.context or {},
        )
        return DecryptionResponse(
            plaintext=response["Plaintext"],
            key_id=response["KeyId"],
        )
    except Exception as e:
        return DecryptionResponse(
            plaintext=b"",
            key_id=key_id,
            success=False,
            error=str(e),
        )
