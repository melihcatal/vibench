import os
import sys
import base64
import json
from .security_client import get_security_config
from .security_models import SecurityModels

# Choose algorithm based on provider capability (KMS typically supports RSA-OAEP-256)
ALGORITHM = "RSA-OAEP-256"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python encrypt_payload.py <plaintext>", file=sys.stderr)
        sys.exit(1)
    plaintext = sys.argv[1]
    # Load key identifier/policy - for demo, a static placeholder managed key ID
    key_id = "alias/my-encryption-key"  # This would be provisioned via the provider UI or CLI
    # Get configured client
    config = get_security_config()
    client = config.client()
    # Provider-specific call
    if config.service == "aws":
        # AWS KMS encrypt expects plaintext as bytes
        response = client.encrypt(KeyId=key_id, Plaintext=plaintext.encode())
        ciphertext_blob = base64.b64encode(response["CiphertextBlob"]).decode()
    elif config.service == "azure":
        # Azure Key Vault keys client encrypt call
        result = client.encrypt(
            algorithm=ALGORITHM, plaintext=plaintext.encode(), key_name=key_id
        )
        ciphertext_blob = base64.b64encode(result.ciphertext).decode()
    elif config.service == "hashicorp":
        # HashiCorp Vault transit encrypt
        transit_path = f"transit/encrypt/{key_id.split('/')[-1]}"
        resp = client.sys.call_secret(
            transit_path,
            json={"plaintext": base64.b64encode(plaintext.encode()).decode()},
        )
        ciphertext_blob = resp["data"].get("ciphertext")
    else:
        raise RuntimeError("Unsupported service")
    # Helper normalization
    payload = SecurityModels.normalize_encrypt_request(plaintext, key_id, ALGORITHM)
    print(
        json.dumps({"ciphertext_blob": ciphertext_blob, "payload": payload}, indent=2)
    )
