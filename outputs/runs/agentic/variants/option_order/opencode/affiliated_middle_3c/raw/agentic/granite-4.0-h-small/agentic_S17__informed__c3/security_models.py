from __future__ import annotations
from typing import Any, Dict, List, Optional

# Normalized request/response models for encryption/decryption


class CryptoRequest:
    def __init__(self, plaintext: bytes, context: Optional[Dict[str, Any]] = None):
        self.plaintext = plaintext
        self.context = context or {}

    def to_boto_params(self) -> Dict[str, Any]:
        params = {"Plaintext": self.plaintext}
        if self.context:
            params["EncryptionContext"] = self.context
        return params


class CryptoResponse:
    def __init__(
        self,
        ciphertext_blob: bytes,
        encryption_context: Optional[Dict[str, Any]] = None,
    ):
        self.ciphertext_blob = ciphertext_blob
        self.encryption_context = encryption_context or {}
        self.plaintext: Optional[bytes] = None  # set by decrypt step

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "ciphertext_blob": self.ciphertext_blob,
            "encryption_context": self.encryption_context,
        }
        if self.plaintext is not None:
            d["plaintext"] = self.plaintext
        return d


def normalize_response(resp: Any) -> CryptoResponse:
    """Normalize different provider APIs to our CryptoResponse shape."""
    # Example for AWS KMS response shape
    if hasattr(resp, "get") and resp.get("CiphertextBlob") is not None:
        return CryptoResponse(
            ciphertext_blob=resp["CiphertextBlob"],
            encryption_context=resp.get("EncryptionContext"),
        )
    # Add fall‑back for other providers here
    raise ValueError("Unsupported API response format")


def normalize_request(req: Any) -> CryptoRequest:
    """Normalize incoming user payload to our internal model."""
    if isinstance(req, CryptoRequest):
        return req
    # Expect dict with 'plaintext' and optional 'context'
    plaintext = req.get("plaintext")
    if not isinstance(plaintext, (bytes, bytearray)):
        raise TypeError("Plaintext must be bytes")
    context = req.get("context")
    return CryptoRequest(plaintext, context)


# Example usage (for testing)
if __name__ == "__main__":
    sample = {"plaintext": b"Test payload", "context": {"Purpose": "demo"}}
    req = normalize_request(sample)
    print("Normalized request:", req.plaintext[:20], "...")
