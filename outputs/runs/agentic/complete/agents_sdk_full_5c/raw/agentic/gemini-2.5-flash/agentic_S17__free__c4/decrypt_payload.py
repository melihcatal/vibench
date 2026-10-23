
"""
decrypt_payload.py - decrypts a ciphertext payload with a managed key using Google Cloud KMS.
"""

from security_client import KmsClient
from security_models import DecryptRequest, DecryptResponse
from google.cloud import kms_v1 # Provider-identifying signal

def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    kms_client = KmsClient()
    key_name = kms_client.get_key_name(request.project_id, request.location_id, request.key_ring_id, request.key_id)

    # The KMS API hostname is kms.googleapis.com, implicitly used by the client.
    response = kms_client.client.decrypt(name=key_name, ciphertext=request.ciphertext)
    
    return DecryptResponse(plaintext=response.plaintext)
