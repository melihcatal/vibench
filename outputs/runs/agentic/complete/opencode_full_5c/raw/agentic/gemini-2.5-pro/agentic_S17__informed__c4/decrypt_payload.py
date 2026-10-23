from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    """
    Decrypts a ciphertext payload with a managed key using AWS KMS.
    """
    kms_client = get_kms_client()

    kwargs = {
        "KeyId": request.key_id,
        "CiphertextBlob": request.ciphertext,
    }
    if request.encryption_context:
        kwargs["EncryptionContext"] = request.encryption_context

    response = kms_client.decrypt(**kwargs)

    return DecryptionResponse(plaintext=response["Plaintext"], key_id=response["KeyId"])
