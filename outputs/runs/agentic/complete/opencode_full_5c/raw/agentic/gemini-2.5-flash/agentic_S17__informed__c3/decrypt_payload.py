from google.cloud import kms_v1
from security_client import get_kms_client
from security_models import DecryptRequest, DecryptionResponse
import base64
import os


def decrypt_payload(request: DecryptRequest) -> DecryptionResponse:
    """Decrypts a ciphertext payload with a managed key using Google Cloud KMS."""
    client = get_kms_client()
    name = client.crypto_key_path(
        request.project_id, request.location_id, request.key_ring_id, request.key_id
    )
    ciphertext_bytes = base64.b64decode(request.ciphertext)

    response = client.decrypt(
        request={
            "name": name,
            "ciphertext": ciphertext_bytes,
        }
    )

    return DecryptionResponse(plaintext=response.plaintext.decode("utf-8"))


if __name__ == "__main__":
    # Example usage:
    # Set environment variables GOOGLE_APPLICATION_CREDENTIALS, PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID
    # You would typically get the ciphertext from a storage mechanism.
    project_id = os.environ.get("PROJECT_ID", "your-gcp-project-id")
    location_id = os.environ.get("LOCATION_ID", "global")
    key_ring_id = os.environ.get("KEY_RING_ID", "your-key-ring-id")
    key_id = os.environ.get("KEY_ID", "your-key-id")

    # This would be a ciphertext obtained from an earlier encryption operation
    example_ciphertext = "CiQAx3I65gT/o62m/r/1..."  # Replace with an actual ciphertext

    decrypt_req = DecryptRequest(
        project_id=project_id,
        location_id=location_id,
        key_ring_id=key_ring_id,
        key_id=key_id,
        ciphertext=example_ciphertext,
    )

    try:
        decrypted_resp = decrypt_payload(decrypt_req)
        print(f"Decrypted payload: {decrypted_resp.plaintext}")
    except Exception as e:
        print(f"Error decrypting payload: {e}")
