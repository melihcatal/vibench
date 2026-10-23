"""
sign_or_verify_key.py - uses a managed key service (AWS KMS) for signing or verification.
"""
import base64
from security_client import get_kms_client
from security_models import SignRequest, VerifyRequest

def sign_payload(request: SignRequest) -> str:
    """
    Signs a message using an asymmetric KMS key.

    Args:
        request: A SignRequest object containing key_id, message, signing_algorithm, and message_type.

    Returns:
        The base64 encoded signature as a string.
    """
    kms_client = get_kms_client()
    try:
        response = kms_client.sign(
            KeyId=request.key_id,
            Message=request.message,
            SigningAlgorithm=request.signing_algorithm,
            MessageType=request.message_type
        )
        return base64.b64encode(response['Signature']).decode('utf-8')
    except Exception as e:
        print(f"Error signing payload: {e}")
        raise

def verify_signature(request: VerifyRequest) -> bool:
    """
    Verifies a digital signature using an asymmetric KMS key.

    Args:
        request: A VerifyRequest object containing key_id, message, signature, signing_algorithm, and message_type.

    Returns:
        True if the signature is valid, False otherwise.
    """
    kms_client = get_kms_client()
    try:
        # The signature is expected to be base64 encoded from the signing step
        decoded_signature = base64.b64decode(request.signature)

        response = kms_client.verify(
            KeyId=request.key_id,
            Message=request.message,
            Signature=decoded_signature,
            SigningAlgorithm=request.signing_algorithm,
            MessageType=request.message_type
        )
        return response['SignatureValid']
    except Exception as e:
        print(f"Error verifying signature: {e}")
        # In case of verification failure or malformed signature, KMS might raise an error
        return False
