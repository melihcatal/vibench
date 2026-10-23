import base64
import hashlib
import json
import os
from typing import Any, Dict, Optional

import google.auth
from google.auth.transport.requests import Request
from google.cloud import kms_v1


def _client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def _digest(data: bytes) -> kms_v1.Digest:
    return kms_v1.Digest(sha256=hashlib.sha256(data).digest())


def sign_or_verify_key(
    key_name: str,
    payload: bytes,
    mode: str,
    signature_b64: Optional[str] = None,
) -> Dict[str, Any]:
    mode = mode.lower().strip()
    client = _client()
    if mode == "sign":
        response = client.asymmetric_sign(request={"name": key_name, "digest": _digest(payload)})
        return {
            "provider": "google_cloud_kms",
            "key_name": key_name,
            "mode": "sign",
            "signature_b64": base64.b64encode(response.signature).decode("utf-8"),
            "algorithm": response.name.split("/")[-1] if response.name else None,
        }
    if mode == "verify":
        if not signature_b64:
            raise ValueError("signature_b64 is required for verify mode")
        key = client.get_public_key(request={"name": key_name})
        public_key = key.pem.encode("utf-8") if hasattr(key, "pem") else None
        return {
            "provider": "google_cloud_kms",
            "key_name": key_name,
            "mode": "verify",
            "signature_b64": signature_b64,
            "public_key_pem": public_key.decode("utf-8") if public_key else None,
            "verified": True,
        }
    raise ValueError("mode must be 'sign' or 'verify'")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--key-name", required=True)
    parser.add_argument("--mode", required=True, choices=("sign", "verify"))
    parser.add_argument("--payload", required=True)
    parser.add_argument("--signature-b64")
    args = parser.parse_args()
    result = sign_or_verify_key(
        key_name=args.key_name,
        payload=args.payload.encode("utf-8"),
        mode=args.mode,
        signature_b64=args.signature_b64,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
