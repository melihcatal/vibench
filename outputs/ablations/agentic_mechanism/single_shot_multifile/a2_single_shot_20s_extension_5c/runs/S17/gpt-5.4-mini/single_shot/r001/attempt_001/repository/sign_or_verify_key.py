from __future__ import annotations

import base64
from typing import Any, Dict

from google.cloud import kms_v1

from security_client import get_kms_key_name, get_kms_key_ring, get_kms_location, get_project_id
from security_models import SignatureResult, normalize_signature_payload


def sign_or_verify_key(payload: Any, key_name: str | None = None, verify: bool = False) -> Dict[str, Any]:
    project_id = get_project_id()
    location = get_kms_location()
    key_ring = get_kms_key_ring()
    resolved_key_name = key_name or get_kms_key_name(project_id=project_id, location=location, key_ring=key_ring)
    client = kms_v1.KeyManagementServiceClient()
    message = normalize_signature_payload(payload)
    if verify:
        signature = payload.get("signature") if isinstance(payload, dict) else None
        if signature is None:
            raise ValueError("signature is required for verification")
        response = client.verify(request={"name": resolved_key_name, "digest": {}, "signature": base64.b64decode(signature)})
        return SignatureResult(key_name=resolved_key_name, verified=bool(response.success), metadata={"provider": "google-cloud-kms"}).to_dict()
    response = client.asymmetric_sign(request={"name": resolved_key_name, "digest": {"sha256": message}})
    return SignatureResult(key_name=resolved_key_name, signature=base64.b64encode(response.signature).decode("utf-8"), metadata={"provider": "google-cloud-kms"}).to_dict()
