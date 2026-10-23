"""Local request, response, and normalization helpers for Managed Object Storage."""

import hashlib
from datetime import datetime, timezone


class UploadRequest:
    """Normalized upload request model."""

    def __init__(self, bucket, key, body, content_type=None, metadata=None, acl=None):
        self.bucket = bucket
        self.key = key
        self.body = body
        self.content_type = content_type or "application/octet-stream"
        self.metadata = metadata or {}
        self.acl = acl

    def to_s3_kwargs(self):
        """Convert to boto3 put_object keyword arguments."""
        kwargs = {
            "Bucket": self.bucket,
            "Key": self.key,
            "Body": self.body,
            "ContentType": self.content_type,
            "Metadata": {k: str(v) for k, v in self.metadata.items()},
        }
        if self.acl:
            kwargs["ACL"] = self.acl
        return kwargs


class UploadResponse:
    """Normalized upload response model."""

    def __init__(self, bucket, key, etag=None, version_id=None, content_length=None):
        self.bucket = bucket
        self.key = key
        self.etag = etag
        self.version_id = version_id
        self.content_length = content_length
        self.timestamp = datetime.now(timezone.utc)

    @classmethod
    def from_s3_response(cls, s3_response, bucket, key):
        """Create from a boto3 put_object response dict."""
        return cls(
            bucket=bucket,
            key=key,
            etag=s3_response.get("ETag", "").strip('"'),
            version_id=s3_response.get("VersionId"),
            content_length=s3_response.get("ContentLength"),
        )

    def to_dict(self):
        return {
            "bucket": self.bucket,
            "key": self.key,
            "etag": self.etag,
            "version_id": self.version_id,
            "content_length": self.content_length,
            "timestamp": self.timestamp.isoformat(),
        }


class ObjectMetadataResult:
    """Normalized object metadata / head result."""

    def __init__(self, bucket, key, size=None, content_type=None, last_modified=None,
                 etag=None, version_id=None, storage_class=None, user_metadata=None,
                 delete_marker=None):
        self.bucket = bucket
        self.key = key
        self.size = size
        self.content_type = content_type
        self.last_modified = last_modified
        self.etag = etag
        self.version_id = version_id
        self.storage_class = storage_class
        self.user_metadata = user_metadata or {}
        self.delete_marker = delete_marker

    @classmethod
    def from_s3_head(cls, head_response, bucket, key):
        """Create from a boto3 head_object response dict."""
        last_modified = head_response.get("LastModified")
        if isinstance(last_modified, datetime):
            last_modified = last_modified.isoformat()
        return cls(
            bucket=bucket,
            key=key,
            size=head_response.get("ContentLength"),
            content_type=head_response.get("ContentType"),
            last_modified=last_modified,
            etag=head_response.get("ETag", "").strip('"'),
            version_id=head_response.get("VersionId"),
            storage_class=head_response.get("StorageClass"),
            user_metadata=head_response.get("Metadata", {}),
            delete_marker=head_response.get("DeleteMarker", False),
        )

    def to_dict(self):
        return {
            "bucket": self.bucket,
            "key": self.key,
            "size": self.size,
            "content_type": self.content_type,
            "last_modified": self.last_modified,
            "etag": self.etag,
            "version_id": self.version_id,
            "storage_class": self.storage_class,
            "user_metadata": self.user_metadata,
            "delete_marker": self.delete_marker,
        }


class PresignedUrlResult:
    """Normalized presigned URL result."""

    def __init__(self, url, bucket, key, expires_in, method="GET"):
        self.url = url
        self.bucket = bucket
        self.key = key
        self.expires_in = expires_in
        self.method = method
        self.generated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return {
            "url": self.url,
            "bucket": self.bucket,
            "key": self.key,
            "expires_in_seconds": self.expires_in,
            "method": self.method,
            "generated_at": self.generated_at,
        }


class ListPrefixResult:
    """Normalized list-prefix result."""

    def __init__(self, bucket, prefix, objects=None, common_prefixes=None,
                 is_truncated=False, next_continuation_token=None):
        self.bucket = bucket
        self.prefix = prefix
        self.objects = objects or []
        self.common_prefixes = common_prefixes or []
        self.is_truncated = is_truncated
        self.next_continuation_token = next_continuation_token

    @classmethod
    def from_s3_list(cls, list_response, bucket, prefix):
        """Create from a boto3 list_objects_v2 response dict."""
        objects = []
        for obj in list_response.get("Contents", []):
            objects.append({
                "key": obj["Key"],
                "size": obj.get("Size"),
                "last_modified": obj.get("LastModified").isoformat() if isinstance(obj.get("LastModified"), datetime) else obj.get("LastModified"),
                "etag": obj.get("ETag", "").strip('"'),
                "storage_class": obj.get("StorageClass"),
            })
        common_prefixes = [p.get("Prefix") for p in list_response.get("CommonPrefixes", [])]
        return cls(
            bucket=bucket,
            prefix=prefix,
            objects=objects,
            common_prefixes=common_prefixes,
            is_truncated=list_response.get("IsTruncated", False),
            next_continuation_token=list_response.get("NextContinuationToken"),
        )

    def to_dict(self):
        return {
            "bucket": self.bucket,
            "prefix": self.prefix,
            "object_count": len(self.objects),
            "objects": self.objects,
            "common_prefixes": self.common_prefixes,
            "is_truncated": self.is_truncated,
            "next_continuation_token": self.next_continuation_token,
        }


class AssetEmbedding:
    """Normalized embedding result for metadata + extracted text search."""

    def __init__(self, object_uri, metadata_vector=None, text_vector=None,
                 model_name=None, combined_vector=None, dimensions=None):
        self.object_uri = object_uri
        self.metadata_vector = metadata_vector or []
        self.text_vector = text_vector or []
        self.combined_vector = combined_vector or []
        self.model_name = model_name
        self.dimensions = dimensions

    def to_dict(self):
        return {
            "object_uri": self.object_uri,
            "metadata_vector_dim": len(self.metadata_vector),
            "text_vector_dim": len(self.text_vector),
            "combined_vector_dim": len(self.combined_vector),
            "model_name": self.model_name,
            "dimensions": self.dimensions,
        }


class OCRResult:
    """Normalized OCR extraction result."""

    def __init__(self, object_uri, text="", blocks=None, confidence=None, pages=None):
        self.object_uri = object_uri
        self.text = text
        self.blocks = blocks or []
        self.confidence = confidence
        self.pages = pages or []

    def to_dict(self):
        return {
            "object_uri": self.object_uri,
            "text": self.text,
            "confidence": self.confidence,
            "page_count": len(self.pages),
        }


class TranslationResult:
    """Normalized translation result."""

    def __init__(self, source_text, translated_text, source_language=None,
                 target_language=None, model_id=None):
        self.source_text = source_text
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language
        self.model_id = model_id

    def to_dict(self):
        return {
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "model_id": self.model_id,
        }


class AssetSummary:
    """Normalized asset summary result."""

    def __init__(self, object_uri, summary="", key_phrases=None, entities=None,
                 model_id=None, word_count=0):
        self.object_uri = object_uri
        self.summary = summary
        self.key_phrases = key_phrases or []
        self.entities = entities or []
        self.model_id = model_id
        self.word_count = word_count

    def to_dict(self):
        return {
            "object_uri": self.object_uri,
            "summary": self.summary,
            "key_phrases": self.key_phrases,
            "entity_count": len(self.entities),
            "word_count": self.word_count,
            "model_id": self.model_id,
        }
