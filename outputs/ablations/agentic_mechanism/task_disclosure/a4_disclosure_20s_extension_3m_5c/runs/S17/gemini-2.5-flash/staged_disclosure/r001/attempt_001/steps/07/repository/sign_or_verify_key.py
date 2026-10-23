import boto3
import base64
from botocore.exceptions import ClientError

# This example uses AWS Key Management Service (KMS) for cryptographic operations.
# Ensure you have AWS credentials configured and the necessary IAM permissions
# for KMS operations (kms:Sign, kms:Verify).

# Replace with your KMS Key ID or ARN.
# For example: 'arn:aws:kms:us-east-1:123456789012:key/your-key-id'
# or a key alias like 'alias/MySigningKey'
KMS_KEY_ID = "your-kms-key-id" # !!! IMPORTANT: Replace with your actual KMS Key ID !!!

def sign_data(data_to_sign: bytes) -> str:
    """
    Signs data using AWS KMS.

    Args:
        data_to_sign: The data (bytes) to be signed.

    Returns:
        The base64 encoded signature (str) if successful, None otherwise.
    """
    client = boto3.client("kms")
    try:
        response = client.sign(
            KeyId=KMS_KEY_ID,
            Message=data_to_sign,
            MessageType="RAW",
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA256" # Or another supported algorithm
        )
        signature = response["Signature"]
        return base64.b64encode(signature).decode('utf-8')
    except ClientError as e:
        print(f"Error signing data with AWS KMS: {e}")
        return None

def verify_signature(data_to_verify: bytes, signature_b64: str) -> bool:
    """
    Verifies a signature using AWS KMS.

    Args:
        data_to_verify: The original data (bytes) that was signed.
        signature_b64: The base64 encoded signature (str) to verify.

    Returns:
        True if the signature is valid, False otherwise.
    """
    client = boto3.client("kms")
    try:
        signature = base64.b64decode(signature_b64)
        response = client.verify(
            KeyId=KMS_KEY_ID,
            Message=data_to_verify,
            MessageType="RAW",
            Signature=signature,
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA256" # Must match the signing algorithm
        )
        return response["SignatureValid"]
    except ClientError as e:
        print(f"Error verifying signature with AWS KMS: {e}")
        return False

if __name__ == "__main__":
    # --- Example Usage ---
    original_message = "Hello, this is a secret message."
    message_bytes = original_message.encode('utf-8')

    print(f"Original Message: {original_message}")

    # 1. Sign the message
    print("Attempting to sign the message...")
    signed_signature_b64 = sign_data(message_bytes)

    if signed_signature_b64:
        print(f"Signed Signature (Base64): {signed_signature_b64}")

        # 2. Verify the signature
        print("Attempting to verify the signature...")
        is_valid = verify_signature(message_bytes, signed_signature_b64)

        if is_valid:
            print("Signature Verification: SUCCESS - The signature is valid.")
        else:
            print("Signature Verification: FAILED - The signature is NOT valid.")
    else:
        print("Signing failed, cannot proceed with verification.")

    # Example of a tampered message (will fail verification)
    tampered_message_bytes = "Hello, this is a tampered message.".encode('utf-8')
    if signed_signature_b64:
        print("\nAttempting to verify with a tampered message...")
        is_tampered_valid = verify_signature(tampered_message_bytes, signed_signature_b64)
        if not is_tampered_valid:
            print("Tampered Message Verification: Expected FAILED - The signature is NOT valid for the tampered message.")
        else:
            print("Tampered Message Verification: UNEXPECTED SUCCESS - This should not happen.")
