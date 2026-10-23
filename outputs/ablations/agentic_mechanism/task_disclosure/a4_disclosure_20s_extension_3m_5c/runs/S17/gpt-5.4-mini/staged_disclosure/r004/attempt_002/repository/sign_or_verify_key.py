import base64
import os
from typing import Optional

from google.cloud import kms_v1
from google.cloud.kms_v1.types import Digest, AsymmetricSignRequest, AsymmetricVerifyRequest, CryptoKeyVersion


def _client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def sign_with_cloud_kms(key_version_name: str, message: bytes) -> str:
    client = _client()
    digest = Digest(sha256=__import__("hashlib").sha256(message).digest())
    response = client.asymmetric_sign(request=AsymmetricSignRequest(name=key_version_name, digest=digest))
    return base64.b64encode(response.signature).decode("ascii")


def verify_with_cloud_kms(key_version_name: str, message: bytes, signature_b64: str) -> bool:
    client = _client()
    digest = Digest(sha256=__import__("hashlib").sha256(message).digest())
    signature = base64.b64decode(signature_b64)
    response = client.asymmetric_verify(
        request=AsymmetricVerifyRequest(name=key_version_name, digest=digest, signature=signature)
    )
    return response.name == key_version_name and response.success


def main() -> None:
    key_version_name = os.environ.get("GOOGLE_CLOUD_KMS_KEY_VERSION")
    message = os.environ.get("MESSAGE", "").encode("utf-8")
    signature_b64 = os.environ.get("SIGNATURE_B64")

    if not key_version_name:
        raise SystemExit("GOOGLE_CLOUD_KMS_KEY_VERSION is required")

    if signature_b64:
        print("verified" if verify_with_cloud_kms(key_version_name, message, signature_b64) else "failed")
    else:
        print(sign_with_cloud_kms(key_version_name, message))


if __name__ == "__main__":
    main()
