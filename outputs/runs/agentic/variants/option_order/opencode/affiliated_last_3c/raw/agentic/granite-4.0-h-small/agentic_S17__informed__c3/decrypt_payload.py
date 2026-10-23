import os
import sys
import base64
import json
from .security_client import get_security_config
from .security_models import SecurityModels

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decrypt_payload.py <ciphertext_blob>", file=sys.stderr)
        sys.exit(1)
    ciphertext_blob = sys.argv[1]
    # Placeholder key ID - in practice this should match the key used to encrypt
    key_id = "alias/my-encryption-key"
    config = get_security_config()
    client = config.client()
    if config.service == "aws":
        response = client.decrypt(CiphertextBlob=base64.b64decode(ciphertext_blob))
        plaintext = SecurityModels.parse_decrypt_response(response)
    elif config.service == "azure":
        result = client.decrypt(
            key_name=key_id, ciphertext=base64.b64decode(ciphertext_blob)
        )
        plaintext = result.plaintext.decode()
    elif config.service == "hashicorp":
        transit_path = f"transit/decrypt/{key_id.split('/')[-1]}"
        resp = client.sys.call_secret(
            transit_path, json={"ciphertext": ciphertext_blob}
        )
        plaintext = SecurityModels.parse_decrypt_response(resp)
    else:
        raise RuntimeError("Unsupported service")
    print(plaintext)
