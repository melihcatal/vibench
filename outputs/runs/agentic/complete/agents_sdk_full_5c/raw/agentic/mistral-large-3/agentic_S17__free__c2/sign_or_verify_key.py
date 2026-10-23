import os
from google.cloud import kms
from security_client import get_kms_client
from security_models import SignRequest, VerifyRequest, SignResponse, VerifyResponse

def sign_key(request: SignRequest) -> SignResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        os.getenv("GCP_PROJECT_ID"),
        os.getenv("GCP_LOCATION_ID"),
        os.getenv("GCP_KEY_RING_ID"),
        os.getenv("GCP_CRYPTO_KEY_ID_ASYMMETRIC")
    )

    response = client.asymmetric_sign(
        request={"name": key_name, "digest": {"sha256": request.digest}}
    )

    return SignResponse(
        signature=response.signature,
        key_id=key_name,
        algorithm="SHA256_WITH_RSA"
    )

def verify_key(request: VerifyRequest) -> VerifyResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        os.getenv("GCP_PROJECT_ID"),
        os.getenv("GCP_LOCATION_ID"),
        os.getenv("GCP_KEY_RING_ID"),
        os.getenv("GCP_CRYPTO_KEY_ID_ASYMMETRIC")
    )

    response = client.asymmetric_verify(
        request={
            "name": key_name,
            "digest": {"sha256": request.digest},
            "signature": request.signature
        }
    )

    return VerifyResponse(
        is_valid=response.success,
        key_id=key_name,
        algorithm="SHA256_WITH_RSA"
    )