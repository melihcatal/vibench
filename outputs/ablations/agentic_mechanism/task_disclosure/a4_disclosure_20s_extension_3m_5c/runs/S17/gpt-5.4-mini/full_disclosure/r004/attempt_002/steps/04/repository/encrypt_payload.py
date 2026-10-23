import base64
import json
import os
from typing import Any, Dict, Optional

from google.cloud import kms_v1


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def encrypt_payload(plaintext: str, key_name: Optional[str] = None) -> Dict[str, Any]:
    client = kms_v1.KeyManagementServiceClient()
    name = key_name or _require_env("GOOGLE_CLOUD_KMS_KEY_NAME")
    plaintext_bytes = plaintext.encode("utf-8")
    response = client.encrypt(request={"name": name, "plaintext": plaintext_bytes})
    return {
        "provider": "google_cloud_kms",
        "key_name": name,
        "ciphertext_b64": base64.b64encode(response.ciphertext).decode("ascii"),
    }


def main() -> None:
    plaintext = _require_env("PLAINTEXT_PAYLOAD")
    key_name = os.getenv("GOOGLE_CLOUD_KMS_KEY_NAME")
    result = encrypt_payload(plaintext, key_name=key_name)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
