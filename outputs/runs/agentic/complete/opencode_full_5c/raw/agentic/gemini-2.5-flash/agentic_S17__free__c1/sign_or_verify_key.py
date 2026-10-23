import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from security_client import get_kms_client
from security_models import SignRequest, VerifyRequest
from google.cloud import kms_v1


def sign_message(request: SignRequest) -> bytes:
    client = get_kms_client()
    key_version_name = client.crypto_key_version_path(
        request.project_id,
        request.location_id,
        request.key_ring_id,
        request.crypto_key_id,
        request.crypto_key_version_id,
    )

    # Google Cloud KMS signal: google.cloud.kms_v1.KeyManagementServiceClient
    # Google Cloud KMS signal: client.asymmetric_sign
    response = client.asymmetric_sign(
        request=kms_v1.AsymmetricSignRequest(
            name=key_version_name, digest={"sha256": request.message}
        )
    )
    return response.signature


def verify_signature(request: VerifyRequest) -> bool:
    client = get_kms_client()
    key_version_name = client.crypto_key_version_path(
        request.project_id,
        request.location_id,
        request.key_ring_id,
        request.crypto_key_id,
        request.crypto_key_version_id,
    )

    # Google Cloud KMS signal: google.cloud.kms_v1.KeyManagementServiceClient
    # Google Cloud KMS signal: client.get_public_key
    public_key_response = client.get_public_key(name=key_version_name)
    public_key = load_pem_public_key(public_key_response.pem.encode("utf-8"))

    try:
        # Assuming SHA256 with PSS padding for example. Actual padding depends on key type.
        public_key.verify(
            request.signature,
            request.message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False
