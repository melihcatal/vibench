from google.cloud import kms_v1
from security_client import get_kms_client, get_key_path
from security_models import EncryptionRequest, EncryptionResponse
import os
import base64


def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    """Encrypts a plaintext payload with a managed key using Google Cloud KMS.

    Args:
        request: An EncryptionRequest object containing the plaintext payload and key ID.

    Returns:
        An EncryptionResponse object with the ciphertext and key ID.
    """
    kms_client = get_kms_client()
    # The KMS key_id should be in the format projects/<PROJECT_ID>/locations/<LOCATION>/keyRings/<KEY_RING_ID>/cryptoKeys/<KEY_ID>
    # For this example, we assume key_id in request is already the full path or can be constructed.
    # For a real application, you might need to parse this or provide project/location/key_ring_id separately.

    # For demonstration purposes, assuming key_id is the full resource name for KMS.
    # In a real scenario, you'd likely get project_id, location_id, keyring_id, and key_name from environment or config.

    # Example of constructing the key path if not provided fully qualified:
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # location_id = os.environ.get("KMS_KEY_LOCATION")
    # key_ring_id = os.environ.get("KMS_KEY_RING_ID")
    # full_key_path = get_key_path(project_id, location_id, key_ring_id, request.key_id)

    # Using the key_id directly from the request, assuming it's a full resource name.
    full_key_path = request.key_id

    try:
        # Convert payload to bytes for encryption
        plaintext_bytes = request.payload.encode("utf-8")

        # Call the KMS API to encrypt the data
        response = kms_client.encrypt(name=full_key_path, plaintext=plaintext_bytes)

        # The ciphertext is returned as bytes, encode it to base64 for string representation
        ciphertext_b64 = base64.b64encode(response.ciphertext).decode("utf-8")

        return EncryptionResponse(ciphertext=ciphertext_b64, key_id=request.key_id)
    except Exception as e:
        # In a real application, you would handle specific KMS exceptions
        raise RuntimeError(f"Error encrypting payload with Google Cloud KMS: {e}")
