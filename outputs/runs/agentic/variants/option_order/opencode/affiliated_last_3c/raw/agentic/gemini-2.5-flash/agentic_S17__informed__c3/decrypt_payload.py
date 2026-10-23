from security_client import get_kms_client
from security_models import DecryptRequest, DecryptResponse
import base64


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    client = get_kms_client()

    if request.additional_authenticated_data:
        aad = request.additional_authenticated_data.encode("utf-8")
    else:
        aad = None

    # Google Cloud KMS decrypts ciphertext. The ciphertext is base64 decoded before passing to KMS.
    # The response contains the plaintext.
    response = client.decrypt(
        request.key_name,
        base64.b64decode(request.ciphertext),
        additional_authenticated_data=aad,
    )

    return DecryptResponse(plaintext=response.plaintext, key_name=request.key_name)
