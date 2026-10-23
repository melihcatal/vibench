import os
import boto3
from security_client import get_kms_client, require_region, resolve_key_id
from security_models import SignRequest, VerifyRequest, SignResponse, VerifyResponse


def sign_or_verify_key(message, key_id=None, region=None, signature=None):
    region = require_region(region)
    client = get_kms_client(region)
    key_id = resolve_key_id(key_id)
    if signature is None:
        request = SignRequest(message=message, key_id=key_id)
        response = client.sign(KeyId=request.key_id, Message=request.message.encode('utf-8'), MessageType='RAW', SigningAlgorithm='RSASSA_PSS_SHA_256')
        return SignResponse(signature=response['Signature'], key_id=response['KeyId'], signing_algorithm=response['SigningAlgorithm']).to_dict()
    request = VerifyRequest(message=message, key_id=key_id, signature=signature)
    response = client.verify(KeyId=request.key_id, Message=request.message.encode('utf-8'), Signature=request.signature, MessageType='RAW', SigningAlgorithm='RSASSA_PSS_SHA_256')
    return VerifyResponse(verified=response['SignatureValid'], key_id=response['KeyId'], signing_algorithm=response['SigningAlgorithm']).to_dict()


if __name__ == '__main__':
    raise SystemExit(0)
