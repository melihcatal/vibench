import base64
from dataclasses import dataclass, asdict

@dataclass
class EncryptionRequest:
    plaintext: str
    project_id: str
    location: str
    key_ring: str
    key_id: str

    def to_dict(self):
        return asdict(self)

@dataclass
class EncryptionResponse:
    ciphertext: bytes

    def to_dict(self):
        return {"ciphertext": base64.b64encode(self.ciphertext).decode('utf-8')}

@dataclass
class DecryptionRequest:
    ciphertext: str
    project_id: str
    location: str
    key_ring: str
    key_id: str

    def to_dict(self):
        return asdict(self)

@dataclass
class DecryptionResponse:
    plaintext: bytes

    def to_dict(self):
        return {"plaintext": self.plaintext.decode('utf-8')}

@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    project_id: str
    location: str
    key_ring: str
    key_id: str

    def to_dict(self):
        return asdict(self)

@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: bytes
    encrypted_data_encryption_key: bytes

    def to_dict(self):
        return {
            "ciphertext": base64.b64encode(self.ciphertext).decode('utf-8'),
            "encrypted_data_encryption_key": base64.b64encode(self.encrypted_data_encryption_key).decode('utf-8')
        }

@dataclass
class SignVerifyRequest:
    message: str
    project_id: str
    location: str
    key_ring: str
    key_id: str
    version_id: str
    signature: str = None

    def to_dict(self):
        return asdict(self)

@dataclass
class SignVerifyResponse:
    result: bool
    signature: bytes = None

    def to_dict(self):
        response_dict = {"result": self.result}
        if self.signature:
            response_dict["signature"] = base64.b64encode(self.signature).decode('utf-8')
        return response_dict
