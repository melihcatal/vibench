from google.cloud import kms_v1
from security_client import get_kms_client
from security_models import EncryptRequest, EncryptionResponse
import base64


def encrypt_payload(request: EncryptRequest) -> EncryptionResponse:
    """Encrypts a plaintext payload with a managed key using Google Cloud KMS."""
    client = get_kms_client()
    name = client.crypto_key_path(
        request.project_id, request.location_id, request.key_ring_id, request.key_id
    )
    plaintext_bytes = request.plaintext.encode("utf-8")

    response = client.encrypt(
        request={
            "name": name,
            "plaintext": plaintext_bytes,
        }
    )

    return EncryptionResponse(
        ciphertext=base64.b64encode(response.ciphertext).decode("utf-8")
    )


if __name__ == "__main__":
    # Example usage:
    # Set environment variables GOOGLE_APPLICATION_CREDENTIALS, PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID
    # For a real scenario, these would come from configuration or environment.
    project_id = os.environ.get("PROJECT_ID", "your-gcp-project-id")
    location_id = os.environ.get("LOCATION_ID", "global")
    key_ring_id = os.environ.get("KEY_RING_ID", "your-key-ring-id")
    key_id = os.environ.get("KEY_ID", "your-key-id")

    plaintext = "This is a secret message."

    encrypt_req = EncryptRequest(
        project_id=project_id,
        location_id=location_id,
        key_ring_id=key_ring_id,
        key_id=key_id,
        plaintext=plaintext,
    )

    try:
        encrypted_resp = encrypt_payload(encrypt_req)
        print(f"Encrypted payload: {encrypted_resp.ciphertext}")
    except Exception as e:
        print(f"Error encrypting payload: {e}")
