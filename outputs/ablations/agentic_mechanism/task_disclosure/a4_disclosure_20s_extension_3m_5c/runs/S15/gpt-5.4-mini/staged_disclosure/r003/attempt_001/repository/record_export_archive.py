import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import boto3


@dataclass
class ArchiveResult:
    bucket: str
    key: str
    etag: Optional[str]
    sha256: str


class RecordExportArchiver:
    def __init__(self, bucket: Optional[str] = None, prefix: str = "exports/archive") -> None:
        self.bucket = bucket or os.environ["S3_EXPORT_ARCHIVE_BUCKET"]
        self.prefix = prefix.strip("/")
        self.s3 = boto3.client("s3")

    def archive_file(self, file_path: str, record_id: str, snapshot_id: Optional[str] = None) -> ArchiveResult:
        path = Path(file_path)
        data = path.read_bytes()
        sha256 = hashlib.sha256(data).hexdigest()
        suffix = path.suffix or ""
        name = path.stem
        parts = [self.prefix, record_id]
        if snapshot_id:
            parts.append(snapshot_id)
        key = "/".join(parts + [f"{name}-{sha256[:16]}{suffix}"])
        extra_args = {}
        content_type = self._content_type_for_suffix(suffix)
        if content_type:
            extra_args["ContentType"] = content_type
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=data, **extra_args)
        head = self.s3.head_object(Bucket=self.bucket, Key=key)
        return ArchiveResult(bucket=self.bucket, key=key, etag=head.get("ETag"), sha256=sha256)

    def archive_bytes(self, payload: bytes, record_id: str, filename: str, snapshot_id: Optional[str] = None) -> ArchiveResult:
        sha256 = hashlib.sha256(payload).hexdigest()
        suffix = Path(filename).suffix or ""
        name = Path(filename).stem
        parts = [self.prefix, record_id]
        if snapshot_id:
            parts.append(snapshot_id)
        key = "/".join(parts + [f"{name}-{sha256[:16]}{suffix}"])
        extra_args = {}
        content_type = self._content_type_for_suffix(suffix)
        if content_type:
            extra_args["ContentType"] = content_type
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=payload, **extra_args)
        head = self.s3.head_object(Bucket=self.bucket, Key=key)
        return ArchiveResult(bucket=self.bucket, key=key, etag=head.get("ETag"), sha256=sha256)

    @staticmethod
    def _content_type_for_suffix(suffix: str) -> Optional[str]:
        mapping = {
            ".pdf": "application/pdf",
            ".json": "application/json",
            ".txt": "text/plain; charset=utf-8",
            ".csv": "text/csv; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".zip": "application/zip",
        }
        return mapping.get(suffix.lower())


def archive_record_export(file_path: str, record_id: str, snapshot_id: Optional[str] = None, bucket: Optional[str] = None) -> ArchiveResult:
    return RecordExportArchiver(bucket=bucket).archive_file(file_path=file_path, record_id=record_id, snapshot_id=snapshot_id)
