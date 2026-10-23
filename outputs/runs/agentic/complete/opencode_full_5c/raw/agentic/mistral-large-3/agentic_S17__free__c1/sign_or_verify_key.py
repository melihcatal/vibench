from google.cloud import kms
import os
import base64
from security_client import EncryptionClient
from security_models import normalize_signing_response, normalize_verification_response


class SigningClient(EncryptionClient):
    def sign_payload(self, payload: str) -> dict:
        payload_bytes = payload.encode("utf-8")
        response = self.client.asymmetric_sign(
            request={
                "name": self.key_name,
                "payload": payload_bytes,
                "digest": {"sha256": payload_bytes},
            }
        )
        return {
            "signature": base64.b64encode(response.signature).decode("utf-8"),
            "key_id": self.key_name,
            "algorithm": "SHA256_WITH_RSA",
        }

    def verify_signature(self, payload: str, signature: str) -> dict:
        payload_bytes = payload.encode("utf-8")
        signature_bytes = base64.b64decode(signature)
        response = self.client.asymmetric_verify(
            request={
                "name": self.key_name,
                "payload": payload_bytes,
                "signature": signature_bytes,
                "digest": {"sha256": payload_bytes},
            }
        )
        return {
            "is_valid": response.success,
            "key_id": self.key_name,
            "algorithm": "SHA256_WITH_RSA",
        }


def sign_payload(payload: str) -> dict:
    client = SigningClient()
    result = client.sign_payload(payload)
    return normalize_signing_response(result).__dict__


def verify_signature(payload: str, signature: str) -> dict:
    client = SigningClient()
    result = client.verify_signature(payload, signature)
    return normalize_verification_response(result).__dict__
