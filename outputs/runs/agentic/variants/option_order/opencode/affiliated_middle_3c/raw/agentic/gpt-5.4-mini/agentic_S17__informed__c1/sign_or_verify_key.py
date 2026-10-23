import base64
import boto3
from security_client import get_kms_client, get_kms_key_id, get_region_name
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse, normalize_message

def sign_or_verify_key(message: str, key_id: str | None = None, signature_b64: str | None = None, region_name: str | None = None):
    kms = get_kms_client(region_name=region_name or get_region_name())
    request_message = normalize_message(message)
    if signature_b64 is None:
        req = SignRequest(message=request_message, key_id=key_id or get_kms_key_id())
        result = kms.sign(KeyId=req.key_id, Message=req.message.encode('utf-8'), MessageType='RAW', SigningAlgorithm='RSASSA_PSS_SHA_256')
        return SignResponse(signature_b64=base64.b64encode(result['Signature']).decode('utf-8'), key_id=req.key_id, provider='aws_kms')
    req = VerifyRequest(message=request_message, key_id=key_id or get_kms_key_id(), signature_b64=signature_b64)
    result = kms.verify(KeyId=req.key_id, Message=req.message.encode('utf-8'), MessageType='RAW', Signature=base64.b64decode(req.signature_b64), SigningAlgorithm='RSASSA_PSS_SHA_256')
    return VerifyResponse(signature_valid=bool(result['SignatureValid']), key_id=req.key_id, provider='aws_kms')
