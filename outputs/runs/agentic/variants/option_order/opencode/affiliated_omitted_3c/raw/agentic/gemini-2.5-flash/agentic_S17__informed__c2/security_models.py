import dataclasses
from typing import Optional


@dataclasses.dataclass
class EncryptRequest:
    plaintext: str
    key_id: str


@dataclasses.dataclass
class EncryptResponse:
    ciphertext: str
    key_id: str
    encryption_algorithm: str


@dataclasses.dataclass
class DecryptRequest:
    ciphertext: str
    key_id: str


@dataclasses.dataclass
class DecryptResponse:
    plaintext: str
    key_id: str
    encryption_algorithm: str


@dataclasses.dataclass
class EnvelopeEncryptRequest:
    plaintext: str
    key_id: str


@dataclasses.dataclass
class EnvelopeEncryptResponse:
    ciphertext_blob: str
    data_key_ciphertext: str
    key_id: str


@dataclasses.dataclass
class SignRequest:
    message: str
    key_id: str
    signing_algorithm: str


@dataclasses.dataclass
class SignResponse:
    signature: str
    key_id: str
    signing_algorithm: str


@dataclasses.dataclass
class VerifyRequest:
    message: str
    signature: str
    key_id: str
    signing_algorithm: str


@dataclasses.dataclass
class SummarizeRequest:
    text: str


@dataclasses.dataclass
class SummarizeResponse:
    summary: str


@dataclasses.dataclass
class ContentSafetyRequest:
    text: str


@dataclasses.dataclass
class ContentSafetyResponse:
    is_safe: bool
    moderation_results: Optional[dict] = None


@dataclasses.dataclass
class EmbeddingRequest:
    text: str


@dataclasses.dataclass
class EmbeddingResponse:
    embedding: list[float]


@dataclasses.dataclass
class TranslateRequest:
    text: str
    target_lang: str
    source_lang: Optional[str] = None


@dataclasses.dataclass
class TranslateResponse:
    translated_text: str
    source_lang: str
    target_lang: str
