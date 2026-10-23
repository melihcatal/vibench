import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class SignOrVerifyResult:
    provider: str
    key_name: str
    operation: str
    success: bool
    signature: Optional[str] = None
    verified: Optional[bool] = None
    raw_response: Optional[Dict[str, Any]] = None


class GoogleCloudKMSClient:
    def __init__(self, project_id: str, location_id: str, key_ring_id: str, key_id: str, key_version_id: str):
        self.project_id = project_id
        self.location_id = location_id
        self.key_ring_id = key_ring_id
        self.key_id = key_id
        self.key_version_id = key_version_id
        self.base_url = "https://cloudkms.googleapis.com/v1"
        self.token = os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN") or os.environ.get("GOOGLE_APPLICATION_ACCESS_TOKEN")
        if not self.token:
            raise ValueError("GOOGLE_OAUTH_ACCESS_TOKEN or GOOGLE_APPLICATION_ACCESS_TOKEN is required")

    def _request(self, method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.request(method, url, headers=headers, data=json.dumps(payload) if payload is not None else None, timeout=30)
        response.raise_for_status()
        return response.json()

    def sign(self, message: bytes) -> SignOrVerifyResult:
        digest_b64 = base64.b64encode(message).decode("utf-8")
        path = (
            f"/projects/{self.project_id}/locations/{self.location_id}/keyRings/{self.key_ring_id}"
            f"/cryptoKeys/{self.key_id}/cryptoKeyVersions/{self.key_version_id}:asymmetricSign"
        )
        raw = self._request("POST", path, {"digest": {"sha256": digest_b64}})
        signature = raw.get("signature")
        return SignOrVerifyResult(
            provider="google_cloud_kms",
            key_name=self.key_id,
            operation="sign",
            success=True,
            signature=signature,
            raw_response=raw,
        )

    def verify(self, message: bytes, signature: str) -> SignOrVerifyResult:
        digest_b64 = base64.b64encode(message).decode("utf-8")
        path = (
            f"/projects/{self.project_id}/locations/{self.location_id}/keyRings/{self.key_ring_id}"
            f"/cryptoKeys/{self.key_id}/cryptoKeyVersions/{self.key_version_id}:asymmetricVerify"
        )
        raw = self._request("POST", path, {"digest": {"sha256": digest_b64}, "signature": signature})
        verified = bool(raw.get("verified", False))
        return SignOrVerifyResult(
            provider="google_cloud_kms",
            key_name=self.key_id,
            operation="verify",
            success=verified,
            verified=verified,
            raw_response=raw,
        )


def _env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"{name} is required")
    return value


def main() -> Dict[str, Any]:
    action = _env("KMS_ACTION").lower()
    project_id = _env("GOOGLE_CLOUD_PROJECT")
    location_id = _env("GOOGLE_CLOUD_KMS_LOCATION")
    key_ring_id = _env("GOOGLE_CLOUD_KMS_KEY_RING")
    key_id = _env("GOOGLE_CLOUD_KMS_KEY_ID")
    key_version_id = os.environ.get("GOOGLE_CLOUD_KMS_KEY_VERSION", "1")
    client = GoogleCloudKMSClient(project_id, location_id, key_ring_id, key_id, key_version_id)
    payload = _env("KMS_PAYLOAD").encode("utf-8")

    if action == "sign":
        result = client.sign(payload)
    elif action == "verify":
        signature = _env("KMS_SIGNATURE")
        result = client.verify(payload, signature)
    else:
        raise ValueError("KMS_ACTION must be sign or verify")

    return {
        "provider": result.provider,
        "key_name": result.key_name,
        "operation": result.operation,
        "success": result.success,
        "signature": result.signature,
        "verified": result.verified,
    }


if __name__ == "__main__":
    print(json.dumps(main()))
