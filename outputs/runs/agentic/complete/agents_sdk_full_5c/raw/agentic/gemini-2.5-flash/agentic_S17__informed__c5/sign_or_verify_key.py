import boto3
import os
import base64
from hashlib import sha256

def sign_payload(key_id: str, message: str) -> bytes:
    """
    Signs a message using an asymmetric KMS key.

    Args:
        key_id: The ARN or alias of the asymmetric KMS key to use for signing.
                Must be a key with KeyUsage 'SIGN_VERIFY' and an appropriate
                CustomerMasterKeySpec, e.g., 'RSA_4096'.
        message: The message to sign.

    Returns:
        The signature blob as bytes.
    """
    kms_client = boto3.client(
        'kms',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
    
    # AWS KMS signing requires the message to be hashed first.
    # The digest algorithm must match the one specified in the signing operation.
    message_digest = sha256(message.encode('utf-8')).digest()

    response = kms_client.sign(
        KeyId=key_id,
        Message=message_digest,
        MessageType='DIGEST',
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA256' # Example algorithm
    )
    return response['Signature']

def verify_signature(key_id: str, message: str, signature: bytes) -> bool:
    """
    Verifies a signature using an asymmetric KMS key.

    Args:
        key_id: The ARN or alias of the asymmetric KMS key used for signing.
        message: The original message that was signed.
        signature: The signature blob to verify.

    Returns:
        True if the signature is valid, False otherwise.
    """
    kms_client = boto3.client(
        'kms',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

    message_digest = sha256(message.encode('utf-8')).digest()

    response = kms_client.verify(
        KeyId=key_id,
        Message=message_digest,
        MessageType='DIGEST',
        Signature=signature,
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA256' # Must match signing algorithm
    )
    return response['SignatureValid']

if __name__ == '__main__':
    # Example usage (requires AWS credentials and an asymmetric KMS key for signing/verification)
    # KMS_SIGNING_KEY_ID should be an asymmetric key with KeyUsage SIGN_VERIFY, e.g., RSA_4096
    
    # signing_key_id = os.environ.get('KMS_SIGNING_KEY_ID')
    # if not signing_key_id:
    #     print("Please set the KMS_SIGNING_KEY_ID environment variable with an asymmetric key for signing.")
    # else:
    #     original_message = "This is a critical audit log entry."
    #     print(f"Original message: {original_message}")
    #     
    #     # Sign the message
    #     signature = sign_payload(signing_key_id, original_message)
    #     print(f"Generated signature (base64 for display): {base64.b64encode(signature).decode()}")
    #     
    #     # Verify the signature
    #     is_valid = verify_signature(signing_key_id, original_message, signature)
    #     print(f"Signature valid: {is_valid}")
    #     
    #     # Test with a tampered message
    #     tampered_message = "This is a critical audit log entry. (TAMPERED)"
    #     is_valid_tampered = verify_signature(signing_key_id, tampered_message, signature)
    #     print(f"Signature valid with tampered message: {is_valid_tampered}")
    #     assert is_valid == True
    #     assert is_valid_tampered == False
