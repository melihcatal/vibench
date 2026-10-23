import base64
from security_client import get_kms_client
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    client = get_kms_client()
    key_name_full = f"projects/{request.key_name.split('/')[1]}/locations/{request.key_name.split('/')[3]}/keyRings/{request.key_name.split('/')[5]}/cryptoKeys/{request.key_name.split('/')[7]}"

    if request.additional_authenticated_data:
        aad_bytes = request.additional_authenticated_data.encode("utf-8")
    else:
        aad_bytes = None

    decrypt_response = client.decrypt(
        name=key_name_full,
        ciphertext=base64.b64decode(request.ciphertext),
        additional_authenticated_data=aad_bytes,
    )

    return DecryptResponse(
        plaintext=decrypt_response.plaintext.decode("utf-8"),
        key_name=request.key_name,
        additional_authenticated_data=request.additional_authenticated_data,
    )
