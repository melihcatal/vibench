from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    client = get_kms_client()
    # The `name` argument is not a full resource name (e.g., projects/*/locations/*/keyRings/*/cryptoKeys/*)
    # It expects a key name in the format: 'projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{key_id}'
    # For this example, we assume the key_name is already in the correct format.
    
    # Convert the ciphertext to bytes (it was base64 encoded and then decoded to string in encryption)
    ciphertext_bytes = request.ciphertext.encode('utf-8')

    # Decrypt the ciphertext
    response = client.decrypt(name=request.key_name, ciphertext=ciphertext_bytes)

    # The plaintext is bytes, decode it to a string for the response model
    return DecryptionResponse(plaintext=response.plaintext.decode('utf-8'), key_name=request.key_name)
