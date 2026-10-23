import base64
import json
import os
from typing import Any, Dict, Optional

from google.cloud import kms_v1


def _b64decode(data: str) -> bytes:
    if data.startswith("base64:"):
        data = data.split("base64:", 1)[1]
    return base64.b64decode(data)


def _b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def sign_or_verify_key(key_name: str, payload: str, operation: str = "sign", signature: Optional[str] = None) -> Dict[str, Any]:
    client = kms_v1.KeyManagementServiceClient()
    message_bytes = payload.encode("utf-8")
    if operation == "sign":
        response = client.asymmetric_sign(request={"name": key_name, "digest": {"sha256": __import__("google.cloud.kms_v1.types").cloud.kms_v1.types.Digest(sha256=__import__("hashlib").sha256(message_bytes).digest())}})
        return {
            "provider": "google_cloud_kms",
            "operation": "sign",
            "key_name": key_name,
            "signature": _b64encode(response.signature),
        }
    if operation == "verify":
        if signature is None:
            raise ValueError("signature is required for verify")
        digest = {"sha256": __import__("hashlib").sha256(message_bytes).digest()}
        sig_bytes = _b64decode(signature)
        response = client.asymmetric_verify(request={"name": key_name, "digest": digest, "signature": sig_bytes})
        return {
            "provider": "google_cloud_kms",
            "operation": "verify",
            "key_name": key_name,
            "verified": bool(response.result),
        }
    raise ValueError("operation must be 'sign' or 'verify'")


def main() -> None:
    key_name = os.environ["GCP_KMS_KEY_NAME"]
    payload = os.environ["PAYLOAD"]
    operation = os.environ.get("OPERATION", "sign")
    signature = os.environ.get("SIGNATURE")
    result = sign_or_verify_key(key_name=key_name, payload=payload, operation=operation, signature=signature)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
