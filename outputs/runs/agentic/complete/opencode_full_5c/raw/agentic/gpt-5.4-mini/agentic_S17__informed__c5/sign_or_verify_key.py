import base64
import hvac
from security_client import build_vault_client
from security_models import SignOrVerifyRequest, SignOrVerifyResponse, normalize_message

def sign_or_verify_key(request: SignOrVerifyRequest) -> SignOrVerifyResponse:
    client = build_vault_client()
    message = normalize_message(request.message)
    if request.operation == 'sign':
        signed = client.secrets.transit.sign_data(
            name=request.key_name,
            hash_algorithm='sha2-256',
            input=base64.b64encode(message.encode('utf-8')).decode('ascii'),
        )
        return SignOrVerifyResponse(signature=signed['data']['signature'], verified=None, key_name=request.key_name)
    verified = client.secrets.transit.verify_data(
        name=request.key_name,
        hash_algorithm='sha2-256',
        input=base64.b64encode(message.encode('utf-8')).decode('ascii'),
        signature=request.signature or '',
    )
    return SignOrVerifyResponse(signature=request.signature, verified=verified['data']['valid'], key_name=request.key_name)
