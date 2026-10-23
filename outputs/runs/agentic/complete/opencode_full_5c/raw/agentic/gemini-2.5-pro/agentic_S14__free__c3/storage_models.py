from dataclasses import dataclass


@dataclass
class S3Object:
    bucket: str
    key: str


@dataclass
class UploadRequest:
    source_file_path: str
    s3_object: S3Object


@dataclass
class PresignedUrlRequest:
    s3_object: S3Object
    expiration_seconds: int


@dataclass
class ObjectMetadata:
    content_type: str
    content_length: int
    e_tag: str
    last_modified: str


@dataclass
class OcrRequest:
    s3_object: S3Object


@dataclass
class TranslateRequest:
    text: str
    source_language_code: str
    target_language_code: str


@dataclass
class SummaryRequest:
    text_content: str


@dataclass
class EmbeddingRequest:
    text_to_embed: str
