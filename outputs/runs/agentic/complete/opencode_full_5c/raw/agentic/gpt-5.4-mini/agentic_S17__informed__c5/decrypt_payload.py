import base64
import hvac
from security_client import build_vault_client, get_vault_kv_context
from security_models import DecryptRequest, DecryptResponse, normalize_ciphertext

def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    client = build_vault_client()
    ctx = get_vault_kv_context()
    response = client.secrets.transit.decrypt_data(
        name=request.key_name,
        ciphertext=normalize_ciphertext(request.ciphertext),
        context=ctx,
    )
    plaintext = base64.b64decode(response['data']['plaintext']).decode('utf-8')
    return DecryptResponse(plaintext=plaintext, key_name=request.key_name)
