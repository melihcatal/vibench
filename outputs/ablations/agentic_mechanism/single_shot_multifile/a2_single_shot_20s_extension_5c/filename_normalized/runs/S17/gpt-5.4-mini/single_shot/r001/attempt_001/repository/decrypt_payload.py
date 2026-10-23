from __future__ import annotations

import base64
from typing import Any, Dict

from google.cloud import kms_v1

from security_client import get_kms_key_name, get_kms_key_ring, get_kms_location, get_project_id
from security_models import DecryptionResult, normalize_ciphertext_payload


def decrypt_payload(payload: Any, key_name: str | None = None) -> Dict[str, Any]:
    project_id = get_project_id()
    location = get_kms_location()
    key_ring = get_kms_key_ring()
    resolved_key_name = key_name or get_kms_key_name(project_id=project_id, location=location, key_ring=key_ring)
    client = kms_v1.KeyManagementServiceClient()
    ciphertext = normalize_ciphertext_payload(payload)
    response = client.decrypt(request={"name": resolved_key_name, "ciphertext": ciphertext})
    result = DecryptionResult(
        key_name=resolved_key_name,
        plaintext=base64.b64encode(response.plaintext).decode("utf-8"),
        metadata={"provider": "google-cloud-kms"},
    )
    return result.to_dict()
