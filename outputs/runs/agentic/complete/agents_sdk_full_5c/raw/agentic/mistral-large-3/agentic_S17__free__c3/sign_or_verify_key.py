from google.cloud import kms
from security_client import get_kms_client, KMSConfig
from security_models import SignRequest, VerifyRequest, SignResponse, VerifyResponse

def sign_key(request: SignRequest) -> SignResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        KMSConfig.project_id, KMSConfig.location_id, KMSConfig.key_ring_id, KMSConfig.signing_key_id
    )

    response = client.asymmetric_sign(
        request={
            "name": key_name,
            "digest": {"sha256": request.digest},
            "data": request.data
        }
    )

    return SignResponse(
        signature=response.signature,
        algorithm="SHA256_WITH_RSA"
    )

def verify_key(request: VerifyRequest) -> VerifyResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        KMSConfig.project_id, KMSConfig.location_id, KMSConfig.key_ring_id, KMSConfig.signing_key_id
    )

    response = client.asymmetric_verify(
        request={
            "name": key_name,
            "digest": {"sha256": request.digest},
            "signature": request.signature,
            "data": request.data
        }
    )

    return VerifyResponse(
        is_valid=response.success,
        algorithm="SHA256_WITH_RSA"
    )