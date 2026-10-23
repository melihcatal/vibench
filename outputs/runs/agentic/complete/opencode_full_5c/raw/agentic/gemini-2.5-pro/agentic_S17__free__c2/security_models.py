from dataclasses import dataclass
from typing import List


@dataclass
class EncryptionPayload:
    key_id: str
    plaintext: bytes


@dataclass
class DecryptionPayload:
    ciphertext: bytes


@dataclass
class EnvelopeEncryptionPayload:
    key_path: str
    plaintext: bytes


@dataclass
class SigningPayload:
    key_id: str
    data_to_sign: bytes


@dataclass
class VerificationPayload:
    key_id: str
    original_data: bytes
    signature: bytes


@dataclass
class ContentSafetyPayload:
    text_content: str


@dataclass
class EmbeddingPayload:
    texts: List[str]
    model: str = "embed-english-v3.0"


@dataclass
class TranslationPayload:
    text: str
    target_lang: str
