import boto3
import os
from security_client import get_kms_client
import hashlib
import base64

def sign_data(message: str, key_id: str, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA256') -> bytes:
    """
    Signs a message using an asymmetric KMS key.
    """
    kms_client = get_kms_client()
    try:
        # AWS KMS requires a digest of the message for signing
        # The digest algorithm must match the signing_algorithm's SHA variant
        message_digest = hashlib.sha256(message.encode('utf-8')).digest()

        response = kms_client.sign(
            KeyId=key_id,
            Message=message_digest,
            MessageType='DIGEST',
            SigningAlgorithm=signing_algorithm
        )
        return response['Signature']
    except Exception as e:
        print(f"Error signing data: {e}")
        raise

def verify_signature(message: str, signature: bytes, key_id: str, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA256') -> bool:
    """
    Verifies a signature using an asymmetric KMS key.
    """
    kms_client = get_kms_client()
    try:
        message_digest = hashlib.sha256(message.encode('utf-8')).digest()

        response = kms_client.verify(
            KeyId=key_id,
            Message=message_digest,
            MessageType='DIGEST',
            Signature=signature,
            SigningAlgorithm=signing_algorithm
        )
        return response['SignatureValid']
    except Exception as e:
        print(f"Error verifying signature: {e}")
        raise

if __name__ == '__main__':
    # Example Usage
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME must be set
    # Ensure AWS_KMS_SIGNING_KEY_ID points to an asymmetric KMS key with SIGN_VERIFY usage.
    kms_signing_key_id = os.environ.get("AWS_KMS_SIGNING_KEY_ID", "alias/MySigningKey")
    example_message = "This message needs to be digitally signed."
    
    # Note: If your key doesn't support RSASSA_PKCS1_V1_5_SHA256,
    # try other algorithms like ECDSA_SHA_256 if your key type is EC_NIST_P256.
    selected_signing_algorithm = 'RSASSA_PKCS1_V1_5_SHA256'

    try:
        print(f"Attempting to sign with Key ID: {kms_signing_key_id} using {selected_signing_algorithm}")
        signature = sign_data(example_message, kms_signing_key_id, selected_signing_algorithm)
        print(f"Signature (base64): {base64.b64encode(signature).decode('utf-8')}")

        is_valid = verify_signature(example_message, signature, kms_signing_key_id, selected_signing_algorithm)
        print(f"Signature is valid: {is_valid}")

        # Test with a modified message
        modified_message = "This message has been tampered with."
        is_valid_modified = verify_signature(modified_message, signature, kms_signing_key_id, selected_signing_algorithm)
        print(f"Signature is valid for modified message (should be False): {is_valid_modified}")

    except Exception as e:
        print(f"Signing or verification failed: {e}")
        print("Please ensure you have an asymmetric KMS key configured for SIGN_VERIFY usage.")
        print("You can create one via AWS Console or CLI: ")
        print("aws kms create-key --key-usage SIGN_VERIFY --key-spec RSA_2048")
        print("Then update AWS_KMS_SIGNING_KEY_ID with the key ARN or alias.")
