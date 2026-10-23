from security_client import get_kms_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_payload(message: bytes, key_id: str, algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256") -> SignResponse:
    """
    Signs a message using AWS KMS.
    
    Args:
        message: The message bytes to sign.
        key_id: The AWS KMS key ID or ARN.
        algorithm: The signing algorithm.
    
    Returns:
        SignResponse containing signature and metadata.
    """
    client = get_kms_client()
    response = client.sign(
        KeyId=key_id,
        Message=message,
        SigningAlgorithm=algorithm
    )
    
    return SignResponse(
        signature=response["Signature"],
        key_id=key_id,
        algorithm=algorithm,
        provider="aws_kms"
    )


def verify_payload(message: bytes, signature: bytes, key_id: str, algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256") -> VerifyResponse:
    """
    Verifies a signature using AWS KMS.
    
    Args:
        message: The original message bytes.
        signature: The signature bytes to verify.
        key_id: The AWS KMS key ID or ARN.
        algorithm: The signing algorithm.
    
    Returns:
        VerifyResponse containing verification result and metadata.
    """
    client = get_kms_client()
    response = client.verify(
        KeyId=key_id,
        Message=message,
        Signature=signature,
        SigningAlgorithm=algorithm
    )
    
    return VerifyResponse(
        is_valid=response["SignatureValid"],
        key_id=key_id,
        algorithm=algorithm,
        provider="aws_kms"
    )