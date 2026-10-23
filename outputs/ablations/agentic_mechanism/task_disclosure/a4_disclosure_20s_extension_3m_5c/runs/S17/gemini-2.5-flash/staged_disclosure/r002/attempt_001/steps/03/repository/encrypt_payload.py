import boto3
import base64

def encrypt_payload_with_kms(plaintext: str, key_id: str) -> bytes:
    """
    Encrypts a plaintext payload using AWS KMS.

    Args:
        plaintext: The plaintext string to encrypt.
        key_id: The ID or ARN of the AWS KMS key to use for encryption.

    Returns:
        The encrypted ciphertext blob in bytes.
    """
    kms_client = boto3.client("kms")
    
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext.encode('utf-8')
    )
    
    return response['CiphertextBlob']

if __name__ == "__main__":
    # Replace with your actual KMS Key ID or ARN
    # Example: "arn:aws:kms:REGION:ACCOUNT_ID:key/YOUR_KEY_ID" or "alias/YOUR_ALIAS_NAME"
    KMS_KEY_ID = "alias/my-encryption-key" # Placeholder

    payload_to_encrypt = "This is a secret message."

    try:
        encrypted_data = encrypt_payload_with_kms(payload_to_encrypt, KMS_KEY_ID)
        print(f"Original Payload: {payload_to_encrypt}")
        print(f"Encrypted Ciphertext (base64-encoded): {base64.b64encode(encrypted_data).decode('utf-8')}")
    except Exception as e:
        print(f"Error encrypting payload: {e}")
        print("Please ensure you have configured your AWS credentials and replaced 'alias/my-encryption-key' with a valid KMS Key ID or ARN.")
