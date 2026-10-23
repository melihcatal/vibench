from google.cloud import kms
from security_client import get_kms_client, KMSConfig
from security_models import SigningRequest, SigningResponse, VerificationRequest, VerificationResponse

def sign_key(request: SigningRequest) -> SigningResponse:
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
            "digest": {"sha256": request.digest},
            "data": request.data
        }
    )

    return SigningResponse(
        signature=response.signature,
        provider="google-cloud-kms",
        model="projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
            request.project_id, request.location_id, request.key_ring_id, request.key_id
        )
    )

def verify_key(request: VerificationRequest) -> VerificationResponse:
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
            "signature": request.signature,
            "data": request.data
        }
    )

    return VerificationResponse(
        is_valid=response.success,
        provider="google-cloud-kms",
        model="projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
            request.project_id, request.location_id, request.key_ring_id, request.key_id
        )
    )