from __future__ import annotations

import base64
from typing import Any, Dict

from google.cloud import kms_v1

from security_client import get_google_kms_client, load_security_config
from security_models import CryptoRequest, CryptoResponse, normalize_text_payload


def encrypt_payload(request: CryptoRequest) -> CryptoResponse:
    config = load_security_config("google_cloud_kms", request.key_name)
    client: kms_v1.KeyManagementServiceClient = get_google_kms_client()
    plaintext = normalize_text_payload(request.plaintext).encode("utf-8")
    name = request.key_name
    response = client.encrypt(request={"name": name, "plaintext": plaintext, "additional_authenticated_data": (request.aad or "").encode("utf-8") if request.aad else None})
    ciphertext = base64.b64encode(response.ciphertext).decode("ascii")
    metadata: Dict[str, Any] = {"provider": "google-cloud-kms", "location": config.location}
    return CryptoResponse(key_name=name, operation="encrypt", payload=ciphertext, metadata=metadata)


if __name__ == "__main__":
    pass
