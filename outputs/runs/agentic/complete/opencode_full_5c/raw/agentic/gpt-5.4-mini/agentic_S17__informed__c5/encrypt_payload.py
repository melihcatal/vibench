import base64
import os
import hvac
from security_client import build_vault_client, get_vault_kv_context
from security_models import EncryptRequest, EncryptResponse, normalize_plaintext

def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    client = build_vault_client()
    ctx = get_vault_kv_context()
    plaintext = normalize_plaintext(request.plaintext)
    response = client.secrets.transit.encrypt_data(
        name=request.key_name,
        plaintext=base64.b64encode(plaintext.encode('utf-8')).decode('ascii'),
        context=ctx,
    )
    return EncryptResponse(ciphertext=response['data']['ciphertext'], key_name=request.key_name)
