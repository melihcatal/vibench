import base64
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class Artifact:
    path: Path
    key: str
    content_type: Optional[str] = None


def _s3_client():
    return boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )


def _guess_content_type(path: Path) -> Optional[str]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "application/json"
    if suffix == ".txt":
        return "text/plain"
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".png":
        return "image/png"
    if suffix == ".webp":
        return "image/webp"
    return None


def _iter_artifacts(input_dir: Path, caption_file: Optional[Path]) -> Iterable[Artifact]:
    for path in sorted(input_dir.rglob("*")):
        if path.is_file():
            rel = path.relative_to(input_dir).as_posix()
            yield Artifact(path=path, key=rel, content_type=_guess_content_type(path))
    if caption_file and caption_file.is_file():
        yield Artifact(path=caption_file, key=caption_file.name, content_type=_guess_content_type(caption_file))


def archive_image_assets(
    bucket: str,
    input_dir: str,
    prefix: str = "image-asset-archive",
    caption_file: Optional[str] = None,
) -> dict:
    s3 = _s3_client()
    src = Path(input_dir)
    caption_path = Path(caption_file) if caption_file else None
    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archived = []
    for artifact in _iter_artifacts(src, caption_path):
        object_key = f"{prefix}/{run_stamp}/{artifact.key}"
        extra_args = {}
        if artifact.content_type:
            extra_args["ContentType"] = artifact.content_type
        s3.upload_file(str(artifact.path), bucket, object_key, ExtraArgs=extra_args or None)
        archived.append({"source": str(artifact.path), "s3_key": object_key})
    manifest = {
        "provider": "aws-s3",
        "bucket": bucket,
        "prefix": prefix,
        "timestamp": run_stamp,
        "items": archived,
    }
    manifest_key = f"{prefix}/{run_stamp}/manifest.json"
    s3.put_object(
        Bucket=bucket,
        Key=manifest_key,
        Body=json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"),
        ContentType="application/json",
    )
    manifest["manifest_key"] = manifest_key
    return manifest


def _load_env_path(name: str) -> Optional[str]:
    value = os.getenv(name)
    return value if value else None


def main() -> int:
    bucket = _load_env_path("ARCHIVE_BUCKET")
    input_dir = _load_env_path("IMAGE_ARTIFACT_DIR")
    if not bucket or not input_dir:
        raise SystemExit("ARCHIVE_BUCKET and IMAGE_ARTIFACT_DIR are required")
    caption_file = _load_env_path("IMAGE_CAPTION_FILE")
    result = archive_image_assets(bucket=bucket, input_dir=input_dir, caption_file=caption_file)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
