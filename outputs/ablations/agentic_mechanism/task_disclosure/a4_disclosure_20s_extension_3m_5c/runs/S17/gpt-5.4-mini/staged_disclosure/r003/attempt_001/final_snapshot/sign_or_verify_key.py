import base64
import hashlib
import os
from typing import Optional

from google.cloud import kms_v1


def _parse_name(name: str) -> str:
    if name.startswith("projects/"):
        return name
    parts = name.split("/")
    if len(parts) != 5:
        raise ValueError("name must be a full Google Cloud KMS key version resource name")
    project, location, key_ring, crypto_key, version = parts
    return f"projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{version}"


def sign_or_verify_key(message: bytes, key_version_name: Optional[str] = None, signature_b64: Optional[str] = None) -> str:
    client = kms_v1.KeyManagementServiceClient()
    name = _parse_name(key_version_name or os.environ["GOOGLE_CLOUD_KMS_KEY_VERSION"])
    digest = hashlib.sha256(message).digest()
    if signature_b64 is None:
        response = client.asymmetric_sign(name=name, digest={"sha256": digest})
        return base64.b64encode(response.signature).decode("ascii")
    signature = base64.b64decode(signature_b64)
    response = client.asymmetric_verify(name=name, digest={"sha256": digest}, signature=signature)
    return "verified" if response.success else "failed"


if __name__ == "__main__":
    import sys

    action = sys.argv[1]
    data = sys.argv[2].encode("utf-8")
    if action == "sign":
        print(sign_or_verify_key(data))
    elif action == "verify":
        print(sign_or_verify_key(data, signature_b64=sys.argv[3]))
    else:
        raise SystemExit("action must be sign or verify")
