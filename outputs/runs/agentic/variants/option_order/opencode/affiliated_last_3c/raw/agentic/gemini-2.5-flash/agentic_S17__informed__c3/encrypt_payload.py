from security_client import get_kms_client
from security_models import EncryptRequest, EncryptResponse
import base64


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    client = get_kms_client()

    if request.additional_authenticated_data:
        aad = request.additional_authenticated_data.encode("utf-8")
    else:
        aad = None

    # Google Cloud KMS encrypts plaintext. The plaintext and any additional_authenticated_data are converted to bytes.
    # The response contains the ciphertext.
    response = client.encrypt(
        request.key_name,
        request.plaintext.encode("utf-8"),
        additional_authenticated_data=aad,
    )

    return EncryptResponse(ciphertext=response.ciphertext, key_name=request.key_name)
