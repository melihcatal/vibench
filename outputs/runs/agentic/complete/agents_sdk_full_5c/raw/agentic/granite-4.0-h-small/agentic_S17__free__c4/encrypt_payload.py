import os
import base64
from google.cloud import kms_v1

from security_client import get_kms_client
from security_models import serialize_request

def encrypt_payload(payload: str, ciphertext_file: str, project_id: str, location: str, key_ring: str, crypto_key: str) -> None:
    """Encrypt a plaintext payload using Google Cloud KMS asymmetric encryption (RSA-OAEP-256).\n\n    Args:\n        payload: plaintext to encrypt.\n        ciphertext_file: file path to write Base64‑encoded ciphertext.\n        project_id, location, key_ring, crypto_key: identifiers for the KMS key.\n    """
    # Load the client (uses GOOGLE_APPLICATION_CREDENTIALS env var)\n    kms_client = get_kms_client()\n    # Build the encrypt request according to the Google KMS API\n    encrypt_req = kms_v1.types.EncryptRequest(\n        name=f\"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}\",\n        plaintext=base64.b64encode(payload.encode('utf-8')).decode('utf-8'),\n        additional_authenticated_data=\"\"  # not used for asymmetric encryption\n    )\n    # Call the service\n    response = kms_client.encrypt(encrypt_req)\n    # Write Base64‑encoded ciphertext to file\n    with open(ciphertext_file, \"wb\") as f:\n        f.write(response.ciphertext)
