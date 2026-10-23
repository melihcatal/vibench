from google.cloud import kms
from security_client import get_kms_client, KMSConfig
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse

def sign_key(request: SignRequest) -> SignResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id, 
        request.location_id, 
        request.key_ring_id, 
        request.key_id
    )

    response = client.asymmetric_sign(
        request={
            "name": key_name,
            "digest": {"sha256": request.digest}
        }
    )

    return SignResponse(
        signature=response.signature
    )

def verify_key(request: VerifyRequest) -> VerifyResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id, 
        request.location_id, 
        request.key_ring_id, 
        request.key_id
    )

    response = client.asymmetric_verify(
        request={
            "name": key_name,
            "digest": {"sha256": request.digest},
            "signature": request.signature
        }
    )

    return VerifyResponse(
        valid=response.success
    )