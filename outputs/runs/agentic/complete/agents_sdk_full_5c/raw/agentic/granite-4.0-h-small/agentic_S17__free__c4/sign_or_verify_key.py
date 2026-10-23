import os
from google.cloud import kms_v1

from security_client import get_kms_client
from security_models import serialize_request

def sign_or_verify_key(project_id: str, location: str, key_ring: str, crypto_key: str, data: str, operation: str = 'SIGN') -> str:
    """Sign or verify data using a managed asymmetric Cloud KMS key.

    Args:
        project_id, location, key_ring, crypto_key: KMS resource identifiers.
        data: string to sign (or verify).\n        operation: 'SIGN' (default) to produce a signature, 'VERIFY' to check a signature.\n\n    Returns:
        For SIGN: the Base64‑encoded signature bytes.
        For VERIFY: \"OK\" if verification succeeds, raises exception otherwise.\n    """
    client = get_kms_client()\n    name = f\"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}\"\n    # Prepare the request payload (bytes)
    payload_bytes = data.encode('utf-8')\n    # Call the appropriate KMS method
    if operation.upper() == 'SIGN':\n        response = client.sign(name=name, plaintext=payload_bytes)\n        return base64.b64encode(response.signature).decode('utf-8')\n    elif operation.upper() == 'VERIFY':\n        # KMS Verify expects the signature to be base64‑encoded string in the request;
        # we re‑encode the provided signature from the caller (here we just illustrate).\n        # In a real workflow you would obtain the signature elsewhere and compare here.\n        verify_req = kms_v1.types.VerifyRequest(\n            name=name,\n            signature=base64.b64encode(payload_bytes).decode('utf-8'),  # placeholder\n            plaintext=payload_bytes\n        )\n        response = client.verify(verify_req)\n        if response.success:\n            return \"OK\"\n        else:\n            raise ValueError(\"Verification failed\")\n    else:\n        raise ValueError(f\"Unknown operation {operation}\")\n