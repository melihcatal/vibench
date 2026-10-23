from google.cloud import kms
from cryptography.fernet import Fernet
import base64
from security_client import get_kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse

def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id, 
        request.location_id, 
        request.key_ring_id, 
        request.key_id
    )
    
    # Generate a data encryption key (DEK)
    dek = Fernet.generate_key()
    fernet = Fernet(dek)
    
    # Encrypt the DEK with Google Cloud KMS
    response = client.encrypt(request={"name": key_name, "plaintext": dek})
    encrypted_dek = response.ciphertext
    
    # Encrypt the plaintext with the DEK
    ciphertext = fernet.encrypt(request.plaintext)
    
    return EnvelopeEncryptResponse(
        ciphertext=ciphertext,
        encrypted_dek=encrypted_dek
    )