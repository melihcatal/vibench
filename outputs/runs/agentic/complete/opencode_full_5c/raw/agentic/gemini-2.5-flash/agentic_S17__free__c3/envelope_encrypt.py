import os
import base64
from cryptography.fernet import Fernet
from security_client import get_kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    client = get_kms_client()
    key_name_full = f"projects/{request.key_name.split('/')[1]}/locations/{request.key_name.split('/')[3]}/keyRings/{request.key_name.split('/')[5]}/cryptoKeys/{request.key_name.split('/')[7]}"

    # Generate a data encryption key (DEK) locally
    data_key = Fernet.generate_key()
    f = Fernet(data_key)

    # Encrypt the DEK with KMS
    if request.additional_authenticated_data:
        aad_bytes = request.additional_authenticated_data.encode("utf-8")
    else:
        aad_bytes = None

    encrypt_dek_response = client.encrypt(
        name=key_name_full, plaintext=data_key, additional_authenticated_data=aad_bytes
    )
    encrypted_data_key = base64.b64encode(encrypt_dek_response.ciphertext).decode(
        "utf-8"
    )

    # Encrypt the actual payload with the locally generated DEK
    ciphertext_payload = f.encrypt(request.plaintext.encode("utf-8")).decode("utf-8")

    return EnvelopeEncryptResponse(
        encrypted_data_key=encrypted_data_key,
        ciphertext=ciphertext_payload,
        key_name=request.key_name,
        additional_authenticated_data=request.additional_authenticated_data,
    )
