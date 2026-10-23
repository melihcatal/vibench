# envelope_encrypt.py
from cryptography.fernet import Fernet
from security_client import get_gcp_kms_client
from security_models import EnvelopeEncryptionResult

def envelope_encrypt_gcp(plaintext: bytes, key_name: str) -> EnvelopeEncryptionResult:
    """
    Performs envelope encryption using a local data key and Google Cloud KMS.
    
    Args:
        plaintext: The data to encrypt.
        key_name: The resource name of the Cloud KMS key to use for wrapping.
                  e.g., projects/PROJECT/locations/LOCATION/keyRings/RING/cryptoKeys/KEY

    Returns:
        An EnvelopeEncryptionResult containing the wrapped data key and ciphertext.
    """
    # 1. Generate a local data key.
    data_key = Fernet.generate_key()

    # 2. Use the data key to encrypt the plaintext.
    f = Fernet(data_key)
    ciphertext = f.encrypt(plaintext)

    # 3. Use Google Cloud KMS to encrypt (wrap) the data key.
    kms_client = get_gcp_kms_client()
    encrypt_response = kms_client.encrypt(
        request={"name": key_name, "plaintext": data_key}
    )
    wrapped_data_key = encrypt_response.ciphertext

    return EnvelopeEncryptionResult(
        wrapped_data_key=wrapped_data_key,
        ciphertext=ciphertext
    )
