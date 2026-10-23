import os
import re
from google.cloud import kms_v1
from security_client import KmsClient
from key_usage_summary import _record_usage, summarize_usage
from payload_safety import is_payload_safe

# Public utility that registers the sign/verify calls and prints usage summary

def sign_message(message: str, key_name: str) -> str:
    """Sign a plaintext message using an asymmetric KMS key.
    Args:
        message (str): Message to sign.
        key_name (str): Full resource name of a KMS crypto key with SIGNATURE usage.
    Returns:
        str: Base64-encoded signature.
    """
    # Call KMS API
    response = KmsClient().asymmetric_sign(key_name, message.encode('utf-8'))
    _record_usage(\"SIGN\")
    return response.signature.decode('utf-8')


def verify_signature(message: str, signature_b64: str, key_name: str) -> bool:
    """Verify a signature produced by an asymmetric KMS key.
    Args:
        message (str): Original plaintext message.
        signature_b64 (str): Base64-encoded signature string.
        key_name (str): Full resource name of the asymmetric KMS key used for signing.
    Returns:
        bool: True if verification succeeds, False otherwise.
    """
    try:
        sig_bytes = base64.b64decode(signature_b64)
        KmsClient().asymmetric_verify(key_name, message.encode('utf-8'), sig_bytes)
    except Exception:
        return False
    _record_usage(\"VERIFY\")
    return True

# Reuse the usage‑summary helper from earlier module
# Provide a simple demo CLI when executed directly
if __name__ == "__main__":
    import json, sys
    if len(sys.argv) < 2:
        print("Usage: python -m sign_or_verify_key {sign|verify} <path-to-json>", file=sys.stderr)
        sys.exit(1)
    action, json_path = sys.argv[1], sys.argv[2]
    with open(json_path, "r") as f:
        data = json.load(f)
    key = data["key"]
    msg = data.get("message")
    if action == "sign":
        print(sign_message(msg, key))
    elif action == "verify":
        sig = data.get("signature")
        if not sig:
            print("Missing signature", file=sys.stderr)
            sys.exit(1)
        print(verify_signature(msg, sig, key))
    else:
        print("Unknown action", file=sys.stderr)
        sys.exit(1)
