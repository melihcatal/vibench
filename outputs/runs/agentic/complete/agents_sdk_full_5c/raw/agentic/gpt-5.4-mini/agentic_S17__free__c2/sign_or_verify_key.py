from __future__ import annotations

import base64
from google.cloud import kms

from security_client import get_kms_client, normalize_key_version_path
from security_models import SignVerifyRequest, CryptoResponse


def sign_or_verify_key(request: SignVerifyRequest) -> CryptoResponse:
    client = get_kms_client()
    key_version_name = normalize_key_version_path(request.key_version_name)
    message = request.message.encode("utf-8")
    if request.signature:
        signature = base64.b64decode(request.signature.encode("utf-8"))
        response = client.asymmetric_verify(request={"name": key_version_name, "digest": {"sha256": __import__("hashlib").sha256(message).digest()}, "signature": signature})
        return CryptoResponse({"verified": str(response.success).lower(), "provider": "google-cloud-kms"})
    response = client.asymmetric_sign(request={"name": key_version_name, "digest": {"sha256": __import__("hashlib").sha256(message).digest()}})
    return CryptoResponse({"signature": base64.b64encode(response.signature).decode("utf-8"), "provider": "google-cloud-kms"})


def main() -> None:
    req = SignVerifyRequest(message="managed key signing")
    print(sign_or_verify_key(req).data)


if __name__ == "__main__":
    main()
