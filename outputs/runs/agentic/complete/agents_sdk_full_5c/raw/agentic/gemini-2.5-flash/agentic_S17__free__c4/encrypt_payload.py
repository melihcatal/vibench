
"""
encrypt_payload.py - encrypts a plaintext payload with a managed key using Google Cloud KMS.
"""

from security_client import KmsClient
from security_models import EncryptRequest, EncryptResponse
from google.cloud import kms_v1 # Provider-identifying signal

def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    kms_client = KmsClient()
    key_name = kms_client.get_key_name(request.project_id, request.location_id, request.key_ring_id, request.key_id)

    # The KMS API hostname is kms.googleapis.com, implicitly used by the client.
    response = kms_client.client.encrypt(name=key_name, plaintext=request.plaintext)
    
    return EncryptResponse(ciphertext=response.ciphertext)
