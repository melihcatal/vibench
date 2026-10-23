from google.cloud import kms
from security_client import get_kms_key_path
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    client = kms.KeyManagementServiceClient()
    name = get_kms_key_path(request.project_id, request.location, request.key_ring, request.key_id)
    
    response = client.decrypt(request={"name": name, "ciphertext": request.ciphertext})
    return DecryptionResponse(plaintext=response.plaintext)
