from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    client = get_kms_client()
    # The `name` argument is not a full resource name (e.g., projects/*/locations/*/keyRings/*/cryptoKeys/*)
    # It expects a key name in the format: 'projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{key_id}'
    # For this example, we assume the key_name is already in the correct format.
    
    # Convert the plaintext to bytes
    plaintext_bytes = request.plaintext.encode('utf-8')

    # Encrypt the plaintext
    response = client.encrypt(name=request.key_name, plaintext=plaintext_bytes)

    # The ciphertext is base64 encoded by the client library, but it's bytes
    # We need to decode it to a string for the response model
    return EncryptionResponse(ciphertext=response.ciphertext.decode('utf-8'), key_name=request.key_name)
