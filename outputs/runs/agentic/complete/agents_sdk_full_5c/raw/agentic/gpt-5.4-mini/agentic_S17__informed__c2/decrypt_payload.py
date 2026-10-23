from __future__ import annotations

import base64
from typing import Any, Dict

from google.cloud import kms_v1

from security_client import get_google_kms_client
from security_models import CryptoRequest, CryptoResponse, normalize_text_payload


def decrypt_payload(request: CryptoRequest) -> CryptoResponse:
    client: kms_v1.KeyManagementServiceClient = get_google_kms_client()
    ciphertext = base64.b64decode(normalize_text_payload(request.ciphertext))
    response = client.decrypt(request={"name": request.key_name, "ciphertext": ciphertext, "additional_authenticated_data": (request.aad or "").encode("utf-8") if request.aad else None})
    payload = response.plaintext.decode("utf-8", errors="replace")
    metadata: Dict[str, Any] = {"provider": "google-cloud-kms"}
    return CryptoResponse(key_name=request.key_name, operation="decrypt", payload=payload, metadata=metadata)


if __name__ == "__main__":
    pass
