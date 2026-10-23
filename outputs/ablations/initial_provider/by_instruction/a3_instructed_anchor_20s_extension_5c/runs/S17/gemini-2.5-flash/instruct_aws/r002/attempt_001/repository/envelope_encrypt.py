from security_client import get_kms_client
from typing import Dict, Any

def envelope_encrypt(plaintext: str, key_id: str, encryption_context: Dict[str, str] = None) -> Dict[str, Any]:
    kms_client = get_kms_client()
    response = kms_client.generate_data_key(
        KeyId=key_id,
        NumberOfBytes=32,  # 256-bit data key
        EncryptionContext=encryption_context or {}
    )
    data_key_plaintext = response['Plaintext']
    encrypted_data_key = response['CiphertextBlob']

    # In a real application, you would use data_key_plaintext to encrypt your actual data locally
    # For this example, we'll just return the encrypted data key and its plaintext (for demonstration)
    # DO NOT expose data_key_plaintext in a real application

    return {
        "encrypted_data_key": encrypted_data_key,
        "data_key_plaintext_base64": data_key_plaintext.decode('utf-8') # For demonstration only, do not return in real app
    }
