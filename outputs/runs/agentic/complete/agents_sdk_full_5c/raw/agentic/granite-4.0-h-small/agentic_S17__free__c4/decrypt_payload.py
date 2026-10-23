import os
import base64
from google.cloud import kms_v1

from security_client import get_kms_client
from security_models import serialize_request

def decrypt_payload(ciphertext_file: str, plaintext_file: str, project_id: str, location: str, key_ring: str, crypto_key: str) -> None:
    """Decrypt a ciphertext payload using Google Cloud KMS asymmetric decryption (RSA-OAEP-256).\n\n    Args:\n        ciphertext_file: file path containing Base64‑encoded ciphertext.\n        plaintext_file: file path to write the resulting plaintext.\n        project_id, location, key_ring, crypto_key: identifiers for the KMS key.\n    """
    kms_client = get_kms_client()\n    with open(ciphertext_file, \"rb\") as f:\n        ciphertext = f.read()\n    decrypt_req = kms_v1.types.DecryptRequest(\n        name=f\"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}\",\n        ciphertext=ciphertext,\n        additional_authenticated_data=\"\"\n    )\n    response = kms_client.decrypt(decrypt_req)\n    with open(plaintext_file, \"wb\") as f:\n        f.write(base64.b64decode(response.plaintext))
