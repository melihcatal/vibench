import boto3
import os
from base64 import b64decode, b64encode

def sign_payload(key_id: str, message: str, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256', region: str = 'us-east-1') -> bytes:
    """
    Signs a message using an asymmetric signing key in AWS KMS.
    """
    kms_client = boto3.client('kms', region_name=region)
    response = kms_client.sign(
        KeyId=key_id,
        Message=message.encode('utf-8'),
        MessageType='RAW',
        SigningAlgorithm=signing_algorithm
    )
    return response['Signature']

def verify_signature(key_id: str, message: str, signature: bytes, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256', region: str = 'us-east-1') -> bool:
    """
    Verifies a signature using an asymmetric signing key in AWS KMS.
    """
    kms_client = boto3.client('kms', region_name=region)
    response = kms_client.verify(
        KeyId=key_id,
        Message=message.encode('utf-8'),
        MessageType='RAW',
        Signature=signature,
        SigningAlgorithm=signing_algorithm
    )
    return response['SignatureValid']

if __name__ == '__main__':
    # This is example usage and should not be part of the final submission.
    # Replace with your actual KMS key ID configured for signing.
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set in environment variables.
    kms_key_id = os.environ.get("KMS_SIGNING_KEY_ID", "alias/MySigningKMSKey")
    example_message = "This message needs to be signed."
    
    # # Example: Sign a message
    # signature = sign_payload(kms_key_id, example_message)
    # print(f"Generated Signature (base64): {b64encode(signature).decode('utf-8')}")
    
    # # Example: Verify the signature
    # is_valid = verify_signature(kms_key_id, example_message, signature)
    # print(f"Signature valid: {is_valid}")
