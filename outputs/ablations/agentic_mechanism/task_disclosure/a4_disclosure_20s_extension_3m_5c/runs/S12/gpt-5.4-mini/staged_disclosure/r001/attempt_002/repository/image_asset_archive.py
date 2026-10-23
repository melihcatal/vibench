import argparse
import base64
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests


S3_ENDPOINT = os.getenv("AWS_S3_ENDPOINT", "https://s3.amazonaws.com")
S3_BUCKET = os.getenv("AWS_S3_BUCKET")
S3_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
DEFAULT_PREFIX = os.getenv("IMAGE_ARCHIVE_PREFIX", "image-asset-archive")


@dataclass(frozen=True)
class ArchiveItem:
    source_path: str
    caption: str
    metadata: Dict[str, Any]


def _require_bucket() -> str:
    if not S3_BUCKET:
        raise ValueError("AWS_S3_BUCKET is required")
    return S3_BUCKET


def _archive_key(prefix: str, source_path: str, suffix: str) -> str:
    stem = Path(source_path).stem
    digest = hashlib.sha256(source_path.encode("utf-8")).hexdigest()[:16]
    return f"{prefix.rstrip('/')}/{stem}-{digest}.{suffix.lstrip('.')}"


def _load_caption(path: Path) -> str:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for key in ("caption", "summary", "description", "text"):
                value = data.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()
            return json.dumps(data, ensure_ascii=False)
        return str(data)
    return path.read_text(encoding="utf-8").strip()


def _build_item(image_path: Path, caption_path: Optional[Path] = None) -> ArchiveItem:
    caption = _load_caption(caption_path) if caption_path else ""
    metadata = {
        "image_file": image_path.name,
        "image_size": image_path.stat().st_size,
    }
    return ArchiveItem(source_path=str(image_path), caption=caption, metadata=metadata)


def _manifest_entry(item: ArchiveItem, image_key: str, caption_key: str, metadata_key: str) -> Dict[str, Any]:
    return {
        "source_path": item.source_path,
        "image_object": image_key,
        "caption_object": caption_key,
        "metadata_object": metadata_key,
        "caption": item.caption,
        "metadata": item.metadata,
    }


def _put_object(session: requests.Session, bucket: str, key: str, body: bytes, content_type: str) -> None:
    url = f"{S3_ENDPOINT.rstrip('/')}/{bucket}/{key}"
    response = session.put(url, data=body, timeout=120, headers={"Content-Type": content_type})
    response.raise_for_status()


def archive_image_artifacts(image_path: str, caption_path: Optional[str] = None, prefix: str = DEFAULT_PREFIX) -> Dict[str, Any]:
    bucket = _require_bucket()
    image_file = Path(image_path)
    if not image_file.is_file():
        raise FileNotFoundError(image_path)
    caption_file = Path(caption_path) if caption_path else None
    item = _build_item(image_file, caption_file)
    session = requests.Session()
    if S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY:
        token_part = f", token={S3_SESSION_TOKEN}" if S3_SESSION_TOKEN else ""
        session.headers.update({"Authorization": f"AWS4-HMAC-SHA256 Credential={S3_ACCESS_KEY_ID}/{S3_REGION}/s3/aws4_request{token_part}"})
    image_key = _archive_key(prefix, item.source_path, image_file.suffix or ".bin")
    caption_key = _archive_key(prefix, item.source_path, "json")
    metadata_key = _archive_key(prefix, item.source_path, "metadata.json")
    _put_object(session, bucket, image_key, image_file.read_bytes(), "application/octet-stream")
    _put_object(session, bucket, caption_key, json.dumps({"caption": item.caption}, ensure_ascii=False).encode("utf-8"), "application/json")
    _put_object(session, bucket, metadata_key, json.dumps(item.metadata, ensure_ascii=False).encode("utf-8"), "application/json")
    manifest = _manifest_entry(item, image_key, caption_key, metadata_key)
    manifest_key = _archive_key(prefix, item.source_path, "manifest.json")
    _put_object(session, bucket, manifest_key, json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"), "application/json")
    manifest["manifest_object"] = manifest_key
    manifest["bucket"] = bucket
    manifest["region"] = S3_REGION
    return manifest


def archive_many(entries: Iterable[Dict[str, Optional[str]]], prefix: str = DEFAULT_PREFIX) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for entry in entries:
        results.append(archive_image_artifacts(entry["image_path"], entry.get("caption_path"), prefix=prefix))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Archive image-analysis artifacts and derived captions to Amazon S3.")
    parser.add_argument("--image", required=True)
    parser.add_argument("--caption")
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    args = parser.parse_args()
    result = archive_image_artifacts(args.image, args.caption, prefix=args.prefix)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
