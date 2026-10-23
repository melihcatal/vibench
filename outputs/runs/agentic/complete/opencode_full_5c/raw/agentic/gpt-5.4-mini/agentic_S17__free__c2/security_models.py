import base64
import json
from dataclasses import dataclass

def normalize_text(value: str) -> str:
    return ' '.join(value.strip().split())

def normalize_b64(value: str) -> str:
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')
@dataclass
class EncryptRequest:
    plaintext: str
    key_name: str
@dataclass
class DecryptRequest:
    ciphertext: str
    key_name: str
@dataclass
class EnvelopeEncryptRequest:
    plaintext: str
    key_name: str
@dataclass
class SignRequest:
    message: str
    key_name: str
@dataclass
class VerifyRequest:
    message: str
    signature: str
    key_name: str
@dataclass
class EncryptResponse:
    ciphertext: str
    key_name: str
    def to_json(self) -> str:
        return json.dumps(self.__dict__)
@dataclass
class DecryptResponse:
    plaintext: str
    key_name: str
    def to_json(self) -> str:
        return json.dumps(self.__dict__)
@dataclass
class EnvelopeEncryptResponse:
    ciphertext: str
    encrypted_dek: str
    key_name: str
    def to_json(self) -> str:
        return json.dumps(self.__dict__)
@dataclass
class SignResponse:
    signature: str
    key_name: str
    def to_json(self) -> str:
        return json.dumps(self.__dict__)
@dataclass
class VerifyResponse:
    valid: bool
    key_name: str
    def to_json(self) -> str:
        return json.dumps(self.__dict__)
