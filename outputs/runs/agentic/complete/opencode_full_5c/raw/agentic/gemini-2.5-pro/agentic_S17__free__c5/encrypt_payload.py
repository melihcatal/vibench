import base64
from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    """Encrypts a plaintext payload using a GCP KMS key."""
    client = get_kms_client()

    response = client.encrypt(
        request={"name": request.key_name, "plaintext": request.plaintext}
    )

    return EncryptionResponse(
        key_name=request.key_name, ciphertext=base64.b64encode(response.ciphertext)
    )
