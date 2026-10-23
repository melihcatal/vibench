import base64
from security_client import get_kms_client
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    client = get_kms_client()
    key_name_full = f"projects/{request.key_name.split('/')[1]}/locations/{request.key_name.split('/')[3]}/keyRings/{request.key_name.split('/')[5]}/cryptoKeys/{request.key_name.split('/')[7]}"

    if request.additional_authenticated_data:
        aad_bytes = request.additional_authenticated_data.encode("utf-8")
    else:
        aad_bytes = None

    encrypt_response = client.encrypt(
        name=key_name_full,
        plaintext=request.plaintext.encode("utf-8"),
        additional_authenticated_data=aad_bytes,
    )

    return EncryptResponse(
        ciphertext=base64.b64encode(encrypt_response.ciphertext).decode("utf-8"),
        key_name=request.key_name,
        additional_authenticated_data=request.additional_authenticated_data,
    )
