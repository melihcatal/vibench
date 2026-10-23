from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    """
    Encrypts a plaintext payload with a managed key using AWS KMS.
    """
    kms_client = get_kms_client()

    kwargs = {
        "KeyId": request.key_id,
        "Plaintext": request.plaintext,
    }
    if request.encryption_context:
        kwargs["EncryptionContext"] = request.encryption_context

    response = kms_client.encrypt(**kwargs)

    return EncryptionResponse(
        ciphertext=response["CiphertextBlob"], key_id=response["KeyId"]
    )
