import os
from security_client import kms_client

def encrypt_payload(plaintext: str) -> dict:
    """Encrypt plaintext using AWS KMS.
    Returns the ciphertext ciphertextBlob and the base64-encoded data key.
    """
    # Use KMS GenerateDataKey to get an encrypted data key
    response = kms_client.generate_data_key(
        KeyId=os.getenv('KMS_KEY_ID'),  # e.g., arn:aws:kms:region:account-id:key/...
        KeySpec='AES_256'
    )
    plaintext_bytes = plaintext.encode('utf-8')
    # Encrypt data with the plaintext data key (local AES for demo)
    import base64, hashlib
    aes_key = hashlib.sha256(response['Plaintext']).digest()  # simple derivation
    from Crypto.Cipher import AES
    cipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext_bytes)
    # Return structure compatible with envelope encryption
    return {
        'ciphertext': base64.b64encode(ciphertext).decode(),
        'iv': base64.b64encode(cipher.nonce).decode(),
        'tag': base64.b64encode(tag).decode(),
        'encrypted_data_key': response['CiphertextBlob']
    }
