import base64
import json
import os
from typing import Any, Dict, Optional

from google.cloud import kms_v1


def decrypt_payload(ciphertext: str, key_name: str, project_id: Optional[str] = None, location_id: Optional[str] = None, key_ring_id: Optional[str] = None, crypto_key_id: Optional[str] = None) -> Dict[str, Any]:
    client = kms_v1.KeyManagementServiceClient()
    if ciphertext.startswith("base64:"):
        ciphertext_bytes = base64.b64decode(ciphertext.split("base64:", 1)[1])
    else:
        ciphertext_bytes = base64.b64decode(ciphertext)
    response = client.decrypt(request={"name": key_name, "ciphertext": ciphertext_bytes})
    plaintext = response.plaintext.decode("utf-8", errors="replace")
    return {"provider": "google_cloud_kms", "key_name": key_name, "plaintext": plaintext}


def main() -> None:
    ciphertext = os.environ["CIPHERTEXT"]
    key_name = os.environ["GCP_KMS_KEY_NAME"]
    result = decrypt_payload(ciphertext=ciphertext, key_name=key_name)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
