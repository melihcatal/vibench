from security_client import get_kms_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_payload(payload: bytes, key_id: str) -> SignResponse:
    """
    Signs a payload using Google Cloud KMS asymmetric signing.
    
    Args:
        payload: The payload bytes to sign.
        key_id: The fully-qualified Google Cloud KMS key identifier.
    
    Returns:
        SignResponse containing signature and metadata.
    """
    client = get_kms_client()
    request = SignRequest(payload=payload, key_id=key_id)
    
    # Google Cloud KMS-specific signing
    from google.cloud import kms
    kms_client = client
    key_name = kms_client.crypto_key_path_path(
        request.key_id.split('/')[1],  # project_id
        request.key_id.split('/')[3],  # location_id
        request.key_id.split('/')[5],  # key_ring_id
        request.key_id.split('/')[7]   # crypto_key_id
    )
    
    response = kms_client.asymmetric_sign(
        request={
            "name": key_name,
            "digest": {"sha256": request.payload}
        }
    )
    
    return SignResponse(
        signature=response.signature,
        key_id=request.key_id,
        algorithm="SHA256_WITH_RSA"
    )


def verify_signature(payload: bytes, signature: bytes, key_id: str) -> VerifyResponse:
    """
    Verifies a signature using Google Cloud KMS asymmetric verification.
    
    Args:
        payload: The original payload bytes.
        signature: The signature bytes to verify.
        key_id: The fully-qualified Google Cloud KMS key identifier.
    
    Returns:
        VerifyResponse containing verification result and metadata.
    """
    client = get_kms_client()
    request = VerifyRequest(payload=payload, signature=signature, key_id=key_id)
    
    # Google Cloud KMS-specific verification
    from google.cloud import kms
    kms_client = client
    key_name = kms_client.crypto_key_path_path(
        request.key_id.split('/')[1],  # project_id
        request.key_id.split('/')[3],  # location_id
        request.key_id.split('/')[5],  # key_ring_id
        request.key_id.split('/')[7]   # crypto_key_id
    )
    
    response = kms_client.asymmetric_verify(
        request={
            "name": key_name,
            "digest": {"sha256": request.payload},
            "signature": request.signature
        }
    )
    
    return VerifyResponse(
        is_valid=response.success,
        key_id=request.key_id,
        algorithm="SHA256_WITH_RSA"
    )