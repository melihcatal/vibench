import base64
import json
import os
from typing import Any, Dict, Optional

import boto3


def _decode_ciphertext(ciphertext: str) -> bytes:
    try:
        return base64.b64decode(ciphertext, validate=True)
    except Exception:
        return ciphertext.encode("utf-8")


def decrypt_payload(ciphertext: str, key_id: Optional[str] = None, encryption_context: Optional[Dict[str, str]] = None, region_name: Optional[str] = None) -> bytes:
    kms = boto3.client("kms", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    kwargs: Dict[str, Any] = {"CiphertextBlob": _decode_ciphertext(ciphertext)}
    if key_id:
        kwargs["KeyId"] = key_id
    if encryption_context:
        kwargs["EncryptionContext"] = encryption_context
    response = kms.decrypt(**kwargs)
    return response["Plaintext"]


def decrypt_payload_text(ciphertext: str, key_id: Optional[str] = None, encryption_context: Optional[Dict[str, str]] = None, region_name: Optional[str] = None, encoding: str = "utf-8") -> str:
    return decrypt_payload(ciphertext, key_id=key_id, encryption_context=encryption_context, region_name=region_name).decode(encoding)


def _main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Decrypt a ciphertext payload with AWS KMS.")
    parser.add_argument("ciphertext", help="Base64 ciphertext blob or raw ciphertext string")
    parser.add_argument("--key-id", dest="key_id")
    parser.add_argument("--region", dest="region_name")
    parser.add_argument("--encryption-context", dest="encryption_context", help='JSON object, e.g. {"purpose":"review"}')
    parser.add_argument("--encoding", default="utf-8")
    args = parser.parse_args()

    encryption_context = json.loads(args.encryption_context) if args.encryption_context else None
    print(decrypt_payload_text(args.ciphertext, key_id=args.key_id, encryption_context=encryption_context, region_name=args.region_name, encoding=args.encoding))


if __name__ == "__main__":
    _main()
