import base64
import os
import hvac
from security_client import build_vault_client, get_vault_kv_context
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse, normalize_plaintext

def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    client = build_vault_client()
    plaintext = normalize_plaintext(request.plaintext).encode('utf-8')
    data_key = os.urandom(32)
    encrypted_payload = bytes(a ^ b for a, b in zip(plaintext, data_key * ((len(plaintext) // len(data_key)) + 1)))
    wrapped = client.secrets.transit.encrypt_data(
        name=request.key_name,
        plaintext=base64.b64encode(data_key).decode('ascii'),
        context=get_vault_kv_context(),
    )
    return EnvelopeEncryptResponse(
        encrypted_payload=base64.b64encode(encrypted_payload).decode('ascii'),
        wrapped_data_key=wrapped['data']['ciphertext'],
        key_name=request.key_name,
    )
