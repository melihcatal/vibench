"""Uses AWS KMS to sign a message digest."""
import os
import base64
import hashlib

from security_client import get_kms_client
from security_models import SigningRequest, SigningResponse

def sign_message(request: SigningRequest) -> SigningResponse:
    """
    Signs a message digest using an asymmetric key in AWS KMS.

    Note: The KMS key must have a KeyUsage of SIGN_VERIFY.
    The message must be hashed beforehand as KMS signs the digest.

    Args:
        request: A SigningRequest object with the message to sign.

    Returns:
        A SigningResponse object with the base64-encoded signature.
    """
    kms_client = get_kms_client()
    # This key ID must correspond to an asymmetric KMS key
    key_id = os.environ.get("KMS_ASYMMETRIC_SIGNING_KEY_ID")
    if not key_id:
        raise ValueError("KMS_ASYMMETRIC_SIGNING_KEY_ID environment variable not set.")

    # KMS sign operation requires a message digest, not the raw message.
    message_hash = hashlib.sha256(request.message).digest()

    response = kms_client.sign(
        KeyId=key_id,
        Message=message_hash,
        MessageType='DIGEST',
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256' # Example algorithm
    )

    signature_blob = response['Signature']
    return SigningResponse(
        message=request.message,
        signature=base64.b64encode(signature_blob).decode('utf-8')
    )

def verify_signature(request: SigningResponse) -> bool:
    """
    Verifies a signature using the public key from AWS KMS.

    Args:
        request: A SigningResponse object containing the message and signature.

    Returns:
        True if the signature is valid, False otherwise.
    """
    kms_client = get_kms_client()
    key_id = os.environ.get("KMS_ASYMMETRIC_SIGNING_KEY_ID")
    if not key_id:
        raise ValueError("KMS_ASYMMETRIC_SIGNING_KEY_ID environment variable not set.")

    message_hash = hashlib.sha256(request.message).digest()
    signature_blob = base64.b64decode(request.signature)

    try:
        response = kms_client.verify(
            KeyId=key_id,
            Message=message_hash,
            MessageType='DIGEST',
            Signature=signature_blob,
            SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
        )
        return response.get('SignatureValid', False)
    except kms_client.exceptions.KMSInvalidSignatureException:
        return False
