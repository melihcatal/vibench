import os
from google.cloud import kms_v1
from security_client import get_kms_key_name, get_kms_client, encode_bytes, decode_bytes
from security_models import SignRequest, VerifyRequest, SignResponse, VerifyResponse

def sign_key(message: str, key_name: str | None = None) -> SignResponse:
    client = get_kms_client()
    name = get_kms_key_name(key_name)
    req = SignRequest(message=message, key_name=name)
    digest = kms_v1.Digest(sha256=bytes(req.message, 'utf-8'))
    response = client.asymmetric_sign(request={"name": req.key_name, "digest": digest})
    return SignResponse(signature=decode_bytes(response.signature), key_name=req.key_name)

def verify_key(message: str, signature: str, key_name: str | None = None) -> VerifyResponse:
    client = get_kms_client()
    name = get_kms_key_name(key_name)
    req = VerifyRequest(message=message, signature=signature, key_name=name)
    digest = kms_v1.Digest(sha256=bytes(req.message, 'utf-8'))
    result = client.asymmetric_verify(request={"name": req.key_name, "digest": digest, "signature": encode_bytes(req.signature)})
    return VerifyResponse(valid=bool(result.successful), key_name=req.key_name)

if __name__ == '__main__':
    message = os.getenv('MESSAGE', '')
    signature = os.getenv('SIGNATURE', '')
    key_name = os.getenv('KMS_KEY_NAME')
    if signature:
        print(verify_key(message, signature, key_name).to_json())
    else:
        print(sign_key(message, key_name).to_json())
