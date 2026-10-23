import os
import sys
import json
import base64
from .security_client import get_security_config
from .security_models import SecurityModels

if __name__ == "__main__":
    # Expect JSON via stdin: {"ciphertext": "", "signature": ""}
    raw = sys.stdin.read()
    data = json.loads(raw)
    ciphertext = data.get("ciphertext")
    signature = data.get("signature")
    if not ciphertext:
        print("Missing ciphertext", file=sys.stderr)
        sys.exit(1)
    if not signature:
        print("Missing signature", file=sys.stderr)
        sys.exit(1)
    key_id = "alias/my-signing-key"  # Placeholder managed key
    config = get_security_config()
    client = config.client()
    if config.service == "aws":
        # Verify using AWS KMS Verify API (requires signature of the plaintext)
        # First we need the plaintext hash; here we sign the raw ciphertext as a simplification
        response = client.verify(
            KeyId=key_id, Message=ciphertext.encode(), Signature=signature.encode()
        )
        result = response["SignatureValid"]
    elif config.service == "azure":
        # Azure Key Vault verify
        verify_result = client.verify_signature(
            key_name=key_id,
            algorithm="RS256",
            value=signature.encode(),
            digest=ciphertext.encode(),
        )
        result = verify_result.value
    elif config.service == "hashicorp":
        # HashiCorp Vault transit verify (Vault supports RSA/ECDSA)
        transit_path = f"transit/verify/{key_id.split('/')[-1]}"
        resp = client.sys.call_secret(
            transit_path,
            json={
                "deactivated": False,
                "public_key": None,  # Vault handles extraction
                "signature": signature.encode(),
                "message": ciphertext.encode(),
            },
        )
        result = resp.get("data", {}).get("valid", False)
    else:
        raise RuntimeError("Unsupported service")
    print(json.dumps({"verified": result}, indent=2))
