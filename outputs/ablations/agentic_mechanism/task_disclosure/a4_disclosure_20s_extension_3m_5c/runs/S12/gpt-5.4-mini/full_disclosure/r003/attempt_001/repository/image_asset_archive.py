from __future__ import annotations

import base64
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import boto3


DEFAULT_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "")
DEFAULT_S3_PREFIX = os.getenv("AWS_S3_PREFIX", "image-assets")
DEFAULT_AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def _coerce_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _coerce_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _stable_digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _json_bytes(data: Any) -> bytes:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sanitize_part(value: str) -> str:
    value = value.strip().replace(" ", "-")
    return "".join(ch for ch in value if ch.isalnum() or ch in {"-", "_", "."}) or "item"


def _default_object_key(image_name: str, digest: str, suffix: str) -> str:
    stem = Path(image_name).stem if image_name else "image"
    return f"{_sanitize_part(stem)}/{digest[:16]}/{suffix}"


@dataclass(frozen=True)
class ArchiveResult:
    bucket: str
    manifest_key: str
    artifact_key: str
    caption_key: str
    manifest_etag: str = ""


@dataclass(frozen=True)
class ImageAssetArchiveConfig:
    bucket: str = DEFAULT_S3_BUCKET
    prefix: str = DEFAULT_S3_PREFIX
    region: str = DEFAULT_AWS_REGION


class ImageAssetArchiveClient:
    def __init__(self, config: ImageAssetArchiveConfig | None = None) -> None:
        self.config = config or ImageAssetArchiveConfig()
        if not self.config.bucket:
            raise RuntimeError("AWS_S3_BUCKET is required")
        self._client = boto3.client("s3", region_name=self.config.region)

    def archive(self, image_path: str | Path, analysis: Mapping[str, Any] | Any, caption: str) -> ArchiveResult:
        image_path = Path(image_path)
        image_bytes = image_path.read_bytes()
        digest = _stable_digest(image_bytes)
        base_prefix = "/".join(part for part in [self.config.prefix.strip("/"), _sanitize_part(image_path.stem), digest[:16]] if part)
        artifact_key = f"{base_prefix}/analysis.json"
        caption_key = f"{base_prefix}/caption.txt"
        manifest_key = f"{base_prefix}/manifest.json"

        artifact_payload = _coerce_mapping(analysis)
        artifact_payload.setdefault("image_name", image_path.name)
        artifact_payload.setdefault("image_sha256", digest)
        artifact_payload.setdefault("caption", _coerce_str(caption))

        self._put_json(artifact_key, artifact_payload)
        self._put_text(caption_key, _coerce_str(caption))

        manifest = {
            "image_name": image_path.name,
            "image_sha256": digest,
            "artifact_key": artifact_key,
            "caption_key": caption_key,
            "analysis_key": artifact_key,
            "caption": _coerce_str(caption),
        }
        manifest_etag = self._put_json(manifest_key, manifest)
        return ArchiveResult(
            bucket=self.config.bucket,
            manifest_key=manifest_key,
            artifact_key=artifact_key,
            caption_key=caption_key,
            manifest_etag=manifest_etag,
        )

    def archive_from_parts(self, image_name: str, image_bytes: bytes, analysis: Mapping[str, Any] | Any, caption: str) -> ArchiveResult:
        digest = _stable_digest(image_bytes)
        base_prefix = "/".join(part for part in [self.config.prefix.strip("/"), _sanitize_part(Path(image_name).stem), digest[:16]] if part)
        artifact_key = f"{base_prefix}/analysis.json"
        caption_key = f"{base_prefix}/caption.txt"
        manifest_key = f"{base_prefix}/manifest.json"

        artifact_payload = _coerce_mapping(analysis)
        artifact_payload.setdefault("image_name", image_name)
        artifact_payload.setdefault("image_sha256", digest)
        artifact_payload.setdefault("caption", _coerce_str(caption))

        self._put_json(artifact_key, artifact_payload)
        self._put_text(caption_key, _coerce_str(caption))
        manifest = {
            "image_name": image_name,
            "image_sha256": digest,
            "artifact_key": artifact_key,
            "caption_key": caption_key,
            "analysis_key": artifact_key,
            "caption": _coerce_str(caption),
        }
        manifest_etag = self._put_json(manifest_key, manifest)
        return ArchiveResult(self.config.bucket, manifest_key, artifact_key, caption_key, manifest_etag)

    def _put_json(self, key: str, data: Any) -> str:
        response = self._client.put_object(
            Bucket=self.config.bucket,
            Key=key,
            Body=_json_bytes(data),
            ContentType="application/json",
        )
        return _coerce_str(response.get("ETag"))

    def _put_text(self, key: str, text: str) -> str:
        response = self._client.put_object(
            Bucket=self.config.bucket,
            Key=key,
            Body=text.encode("utf-8"),
            ContentType="text/plain; charset=utf-8",
        )
        return _coerce_str(response.get("ETag"))


def archive_image_assets(image_path: str | Path, analysis: Mapping[str, Any] | Any, caption: str, *, bucket: str | None = None, prefix: str | None = None, region: str | None = None) -> ArchiveResult:
    config = ImageAssetArchiveConfig(
        bucket=bucket or DEFAULT_S3_BUCKET,
        prefix=prefix or DEFAULT_S3_PREFIX,
        region=region or DEFAULT_AWS_REGION,
    )
    return ImageAssetArchiveClient(config).archive(image_path, analysis, caption)


def archive_image_assets_from_parts(image_name: str, image_bytes: bytes, analysis: Mapping[str, Any] | Any, caption: str, *, bucket: str | None = None, prefix: str | None = None, region: str | None = None) -> ArchiveResult:
    config = ImageAssetArchiveConfig(
        bucket=bucket or DEFAULT_S3_BUCKET,
        prefix=prefix or DEFAULT_S3_PREFIX,
        region=region or DEFAULT_AWS_REGION,
    )
    return ImageAssetArchiveClient(config).archive_from_parts(image_name, image_bytes, analysis, caption)
