import base64
import json
import os
import sys

import boto3


def encrypt_payload(plaintext: str, key_id: str) -> str:
    kms = boto3.client("kms")
    response = kms.encrypt(KeyId=key_id, Plaintext=plaintext.encode("utf-8"))
    return base64.b64encode(response["CiphertextBlob"]).decode("ascii")


def main() -> int:
    if len(sys.argv) < 2:
        sys.stderr.write("usage: encrypt_payload.py <plaintext>\n")
        return 1
    plaintext = sys.argv[1]
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    if not key_id:
        sys.stderr.write("missing AWS_KMS_KEY_ID\n")
        return 1
    result = encrypt_payload(plaintext, key_id)
    sys.stdout.write(json.dumps({"ciphertext": result}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
