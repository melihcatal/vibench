import base64
import json
import os
from typing import Any, Dict, Optional

from google.cloud import kms_v1
from google.api_core.exceptions import GoogleAPICallError


def encrypt_payload(plaintext: str, key_name: Optional[str] = None, plaintext_encoding: str = "utf-8") -> Dict[str, Any]:
    client = kms_v1.KeyManagementServiceClient()
    resource_name = key_name or os.environ.get("GOOGLE_CLOUD_KMS_KEY_NAME")
    if not resource_name:
        raise ValueError("Google Cloud KMS key name is required via key_name or GOOGLE_CLOUD_KMS_KEY_NAME")

    payload = plaintext.encode(plaintext_encoding)
    try:
        response = client.encrypt(request={"name": resource_name, "plaintext": payload})
    except GoogleAPICallError as exc:
        raise RuntimeError(f"Google Cloud KMS encryption failed: {exc}") from exc

    return {
        "provider": "google-cloud-kms",
        "key_name": resource_name,
        "ciphertext_b64": base64.b64encode(response.ciphertext).decode("ascii"),
    }


def main() -> None:
    plaintext = os.environ.get("PLAINTEXT", "")
    result = encrypt_payload(plaintext)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
