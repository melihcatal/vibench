import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

import boto3


@dataclass
class ArchiveResult:
    bucket: str
    uploaded_keys: list[str]


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _iter_image_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff"}:
            yield path


def _caption_path(image_path: Path) -> Optional[Path]:
    candidates = [
        image_path.with_suffix(".txt"),
        image_path.with_suffix(".caption.txt"),
        image_path.with_suffix(".json"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _read_caption(caption_file: Path) -> str:
    if caption_file.suffix.lower() == ".json":
        payload = json.loads(caption_file.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            for key in ("caption", "text", "description"):
                value = payload.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()
        return json.dumps(payload, ensure_ascii=False)
    return caption_file.read_text(encoding="utf-8").strip()


def archive_image_assets(
    source_dir: str,
    bucket_name: str,
    prefix: str = "image-asset-archive",
    region_name: Optional[str] = None,
) -> ArchiveResult:
    s3 = boto3.client("s3", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    root = Path(source_dir)
    uploaded_keys: list[str] = []
    run_prefix = f"{prefix.rstrip('/')}/{_utc_timestamp()}"

    for image_path in _iter_image_files(root):
        rel_image = image_path.relative_to(root).as_posix()
        image_key = f"{run_prefix}/images/{rel_image}"
        s3.upload_file(str(image_path), bucket_name, image_key)
        uploaded_keys.append(image_key)

        caption_file = _caption_path(image_path)
        if caption_file is not None:
            rel_caption = caption_file.relative_to(root).as_posix()
            caption_key = f"{run_prefix}/captions/{rel_caption}"
            s3.put_object(
                Bucket=bucket_name,
                Key=caption_key,
                Body=_read_caption(caption_file).encode("utf-8"),
                ContentType="text/plain; charset=utf-8",
            )
            uploaded_keys.append(caption_key)

    manifest_key = f"{run_prefix}/manifest.json"
    s3.put_object(
        Bucket=bucket_name,
        Key=manifest_key,
        Body=json.dumps(
            {
                "source_dir": str(root),
                "archived_at": _utc_timestamp(),
                "uploaded_keys": uploaded_keys,
                "provider": "aws-s3",
            },
            ensure_ascii=False,
            indent=2,
        ).encode("utf-8"),
        ContentType="application/json",
    )
    uploaded_keys.append(manifest_key)
    return ArchiveResult(bucket=bucket_name, uploaded_keys=uploaded_keys)


def main() -> None:
    source_dir = os.environ.get("IMAGE_ASSET_SOURCE_DIR", ".")
    bucket_name = os.environ["IMAGE_ASSET_BUCKET"]
    prefix = os.environ.get("IMAGE_ASSET_PREFIX", "image-asset-archive")
    region_name = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    archive_image_assets(source_dir, bucket_name, prefix=prefix, region_name=region_name)


if __name__ == "__main__":
    main()
