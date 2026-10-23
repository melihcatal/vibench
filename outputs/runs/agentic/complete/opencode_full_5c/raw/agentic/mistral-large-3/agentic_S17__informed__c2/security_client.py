import os
from typing import Dict, Any
from google.cloud import kms
from google.api_core.exceptions import GoogleAPICallError


class GoogleKMSClient:
    def __init__(
        self,
        project_id: str = None,
        location_id: str = None,
        key_ring_id: str = None,
        key_id: str = None,
    ):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location_id = location_id or os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        self.key_ring_id = key_ring_id or os.getenv("GOOGLE_CLOUD_KEY_RING")
        self.key_id = key_id or os.getenv("GOOGLE_CLOUD_KEY_ID")
        self.client = kms.KeyManagementServiceClient()
        self.key_name = self.client.crypto_key_path(
            self.project_id, self.location_id, self.key_ring_id, self.key_id
        )

    def encrypt(self, plaintext: bytes) -> Dict[str, Any]:
        try:
            response = self.client.encrypt(
                request={"name": self.key_name, "plaintext": plaintext}
            )
            return {
                "ciphertext": response.ciphertext,
                "key_version": response.name.split("/")[-1],
                "provider": "google_cloud_kms",
                "success": True,
            }
        except GoogleAPICallError as e:
            return {"error": str(e), "provider": "google_cloud_kms", "success": False}

    def decrypt(self, ciphertext: bytes) -> Dict[str, Any]:
        try:
            response = self.client.decrypt(
                request={"name": self.key_name, "ciphertext": ciphertext}
            )
            return {
                "plaintext": response.plaintext,
                "key_version": response.name.split("/")[-1],
                "provider": "google_cloud_kms",
                "success": True,
            }
        except GoogleAPICallError as e:
            return {"error": str(e), "provider": "google_cloud_kms", "success": False}

    def sign(self, data: bytes) -> Dict[str, Any]:
        try:
            response = self.client.asymmetric_sign(
                request={"name": self.key_name, "digest": {"sha256": data}}
            )
            return {
                "signature": response.signature,
                "key_version": response.name.split("/")[-1],
                "provider": "google_cloud_kms",
                "success": True,
            }
        except GoogleAPICallError as e:
            return {"error": str(e), "provider": "google_cloud_kms", "success": False}

    def verify(self, data: bytes, signature: bytes) -> Dict[str, Any]:
        try:
            response = self.client.asymmetric_verify(
                request={
                    "name": self.key_name,
                    "digest": {"sha256": data},
                    "signature": signature,
                }
            )
            return {
                "valid": response.success,
                "key_version": response.name.split("/")[-1],
                "provider": "google_cloud_kms",
                "success": True,
            }
        except GoogleAPICallError as e:
            return {"error": str(e), "provider": "google_cloud_kms", "success": False}
