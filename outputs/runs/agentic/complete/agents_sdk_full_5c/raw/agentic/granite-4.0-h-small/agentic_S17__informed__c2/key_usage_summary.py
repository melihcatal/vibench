import os
import base64
import re
from google.cloud import kms_v1
from security_client import KmsClient
from key_usage_summary import summarize_usage
from payload_safety import is_payload_safe

# Public entry point for a key‑usage dashboard
# Reads a line‑separated log file where each line is a JSON payload:
# {"op":"ENCRYPT|DECRYPT|SIGN|VERIFY","key":"<key_name>"}
# and reports counts.

def summarize_key_usage(log_path: str) -> None:
    usage = summarize_usage()
    print("=== Key Usage Summary ===")
    for op, cnt in usage.items():
        print(f"{op}: {cnt}")
    print("--------------------------")


# Example minimal HTTP‑like handler that streams decrypted payloads,
# validates safety, and returns them as a generator.

def stream_decrypted_payloads(request_body: str, key_name: str) -> None:
    """
    request_body: JSON array of objects {"cipher": "base64...", "key":"<key_name>"}
    Streams plaintext for each entry, after safety check.
    """
    import json
    raw = json.loads(request_body)
    if not isinstance(raw, list):
        raise ValueError("Expected JSON array of payload objects.")
    for item in raw:
        cipher_b64 = item.get("cipher")
        entry_key = item.get("key")
        if not cipher_b64 or not entry_key:
            continue  # omit malformed entries
        try:
            plaintext = KmsClient().decrypt(entry_key, base64.b64decode(cipher_b64))
            _record_usage("DECRYPT")
            if not is_payload_safe(plaintext):
                raise ValueError("Payload safety check failed")
            print(plaintext)
        except Exception as exc:
            print(f"FAILED for entry {item}: {exc}", file=sys.stderr)

# The module also registers the same counters with any future calls via the
# KmsClient helpers defined in security_client.py.

if __name__ == "__main__":
    # Simple demo: read a tiny demo log from stdin
    import sys
    log_path = sys.argv[1] if len(sys.argv) > 1 else "log.jsonl"
    summarize_key_usage(log_path)
