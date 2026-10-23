from security_client import sign_with_kms, verify_with_kms, load_config
from security_models import SignOrVerifyRequest, response_map


def sign_or_verify_key(key_id: str, message, signature=None):
    request = SignOrVerifyRequest(key_id=key_id, message=message, signature=signature)
    if request.signature is None:
        signed = sign_with_kms(request.key_id, request.message)
        return response_map(key_id=request.key_id, signature=signed, verified=True)
    verified = verify_with_kms(request.key_id, request.message, request.signature)
    return response_map(key_id=request.key_id, verified=verified)


if __name__ == '__main__':
    config = load_config()
    print(sign_or_verify_key(config['kms_key_id'], ''))
