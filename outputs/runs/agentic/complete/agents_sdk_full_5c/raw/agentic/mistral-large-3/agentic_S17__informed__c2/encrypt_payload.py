from google.cloud import kms
from security_client import get_kms_client
from security_models import EncryptRequest, EncryptResponse

def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id, 
        request.location_id, 
        request.key_ring_id, 
        request.key_id
    )
    
    response = client.encrypt(
        request={"name": key_name, "plaintext": request.plaintext}
    )
    
    return EncryptResponse(ciphertext=response.ciphertext)