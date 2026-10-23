"""
envelope_encrypt.py - implements envelope encryption using a managed key service (AWS KMS).
This file focuses on generating a data key with KMS, which is the KMS-specific part of envelope encryption.
"""
import base64
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest

def generate_envelope_key(request: EnvelopeEncryptionRequest) -> dict:
    """
    Generates a data encryption key and an encrypted copy of that key using AWS KMS.
    This data key can then be used for local encryption of a payload (envelope encryption).

    Args:
        request: An EnvelopeEncryptionRequest object containing key_id, number_of_bytes, and optional encryption_context.

    Returns:
        A dictionary containing the plaintext data key and its encrypted blob,
        both base64 encoded.
    """
    kms_client = get_kms_client()
    try:
        response = kms_client.generate_data_key(
            KeyId=request.key_id,
            NumberOfBytes=request.number_of_bytes,
            EncryptionContext=request.encryption_context if request.encryption_context else {}
        )
        return {
            "PlaintextDataKey": base64.b64encode(response['Plaintext']).decode('utf-8'),
            "EncryptedDataKeyBlob": base64.b64encode(response['CiphertextBlob']).decode('utf-8')
        }
    except Exception as e:
        print(f"Error generating envelope key: {e}")
        raise
