import boto3
import base64

def encrypt_payload(key_id: str, plaintext: str) -> bytes:
    """
    Encrypts a plaintext payload with a managed key using AWS KMS.

    Args:
        key_id: The ID or ARN of the AWS KMS key to use for encryption.
        plaintext: The plaintext payload to encrypt.

    Returns:
        The ciphertext blob as bytes.
    """
    kms_client = boto3.client("kms")
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext.encode("utf-8")
    )
    return response["CiphertextBlob"]

if __name__ == "__main__":
    # This is an example of how to use the function.
    # Replace 'your-kms-key-id' with an actual AWS KMS Key ID or ARN.
    # Ensure your AWS credentials are configured (e.g., via AWS CLI or environment variables).
    
    # Example KMS Key ID (replace with your actual key)
    # key_id_example = "arn:aws:kms:REGION:ACCOUNT_ID:key/YOUR_KEY_ID"
    # key_id_example = "alias/YOUR_ALIAS_NAME"
    key_id_example = "your-kms-key-id" 

    plaintext_example = "This is a secret message."

    try:
        encrypted_data = encrypt_payload(key_id_example, plaintext_example)
        print(f"Original Plaintext: {plaintext_example}")
        print(f"Encrypted Ciphertext (base64): {base64.b64encode(encrypted_data).decode('utf-8')}")
    except Exception as e:
        print(f"Error encrypting payload: {e}")
        print("Please ensure 'your-kms-key-id' is replaced with a valid AWS KMS Key ID or ARN and AWS credentials are configured.")
