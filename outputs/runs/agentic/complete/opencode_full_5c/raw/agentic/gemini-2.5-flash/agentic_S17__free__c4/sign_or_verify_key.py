import os
import base64
from security_client import SecurityClient
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_payload(request: SignRequest) -> SignResponse:
    client = SecurityClient()
    signature = client.sign_with_kms(
        project_id=request.project_id,
        location_id=request.location_id,
        key_ring_id=request.key_ring_id,
        key_id=request.key_id,
        message=request.message,
    )
    return SignResponse(signature=signature)


def verify_payload(request: VerifyRequest) -> VerifyResponse:
    client = SecurityClient()
    is_valid = client.verify_with_kms(
        project_id=request.project_id,
        location_id=request.location_id,
        key_ring_id=request.key_ring_id,
        key_id=request.key_id,
        message=request.message,
        signature=request.signature,
    )
    return VerifyResponse(is_valid=is_valid)
