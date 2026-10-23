import os
from google.cloud import kms_v1
from typing import Any, Dict

class SecurityModels:
    """Local data models for request/response normalization with Google Cloud KMS.
    These classes mirror SDK types but provide helper methods for serialization to/from JSON.
    """
    class EncryptRequest:
        def __init__(self, name: str, plaintext: bytes):
            self.name = name  # KMS crypto key resource path
            self.plaintext = plaintext  # bytes

        def to_sdk(self) -> kms_v1.types.EncryptRequest:
            return kms_v1.types.EncryptRequest(name=self.name, plaintext=self.plaintext)

    class EncryptResponse:
        def __init__(self, ciphertext: bytes):
            self.ciphertext = ciphertext  # bytes

        def from_sdk(self, sdk_resp: kms_v1.types.EncryptResponse) -> None:
            self.ciphertext = sdk_resp.ciphertext

    class DecryptRequest:
        def __init__(self, name: str, ciphertext: bytes):
            self.name = name
            self.ciphertext = ciphertext

        def to_sdk(self) -> kms_v1.types.DecryptRequest:
            return kms_v1.types.DecryptRequest(name=self.name, ciphertext=self.ciphertext)

    class DecryptResponse:
        def __init__(self, plaintext: bytes):
            self.plaintext = plaintext

        def from_sdk(self, sdk_resp: kms_v1.types.DecryptResponse) -> None:
            self.plaintext = sdk_resp.plaintext

    class AsymmetricSignRequest:
        def __init__(self, name: str, message: bytes):
            self.name = name
            self.message = message

        def to_sdk(self) -> kms_v1.types.AsymmetricSignRequest:
            return kms_v1.types.AsymmetricSignRequest(name=self.name, message=self.message)

    class AsymmetricSignResponse:
        def __init__(self, signature: bytes):
            self.signature = signature

        def from_sdk(self, sdk_resp: kms_v1.types.AsymmetricSignResponse) -> None:
            self.signature = sdk_resp.signature

    class AsymmetricVerifyRequest:
        def __init__(self, name: str, message: bytes, signature: bytes):
            self.name = name
            self.message = message
            self.signature = signature

        def to_sdk(self) -> kms_v1.types.AsymmetricVerifyRequest:
            return kms_v1.types.AsymmetricVerifyRequest(name=self.name, message=self.message, signature=self.signature)
