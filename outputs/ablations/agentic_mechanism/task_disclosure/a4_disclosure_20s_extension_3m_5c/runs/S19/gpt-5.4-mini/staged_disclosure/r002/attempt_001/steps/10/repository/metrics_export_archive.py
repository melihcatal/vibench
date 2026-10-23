import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class ArchiveResult:
    source: str
    archive_key: str
    bucket: str


def _s3_client():
    return boto3.client("s3")


def _iter_snapshot_files(source_dir: Path) -> Iterable[Path]:
    for path in sorted(source_dir.iterdir()):
        if path.is_file() and path.suffix in {".json", ".jsonl", ".ndjson", ".csv", ".parquet"}:
            yield path


def archive_metric_snapshots(
    source_dir: str,
    bucket: Optional[str] = None,
    prefix: str = "metric-snapshots/archive",
) -> list[ArchiveResult]:
    bucket_name = bucket or os.environ["AWS_S3_BUCKET"]
    source_path = Path(source_dir)
    if not source_path.is_dir():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    client = _s3_client()
    archived: list[ArchiveResult] = []
    timestamp = datetime.now(timezone.utc).strftime("%Y/%m/%d/%H%M%S")

    for snapshot_file in _iter_snapshot_files(source_path):
        archive_key = f"{prefix}/{timestamp}/{snapshot_file.name}"
        try:
            client.upload_file(str(snapshot_file), bucket_name, archive_key)
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f"Failed to archive {snapshot_file.name} to s3://{bucket_name}/{archive_key}") from exc
        archived.append(ArchiveResult(source=str(snapshot_file), archive_key=archive_key, bucket=bucket_name))

    return archived


def archive_latest_metric_snapshot(
    source_dir: str,
    bucket: Optional[str] = None,
    prefix: str = "metric-snapshots/archive",
) -> Optional[ArchiveResult]:
    archived = archive_metric_snapshots(source_dir=source_dir, bucket=bucket, prefix=prefix)
    return archived[-1] if archived else None


def main() -> None:
    source_dir = os.environ.get("METRICS_EXPORT_DIR", ".")
    bucket = os.environ.get("AWS_S3_BUCKET")
    prefix = os.environ.get("AWS_S3_PREFIX", "metric-snapshots/archive")
    archive_metric_snapshots(source_dir=source_dir, bucket=bucket, prefix=prefix)


if __name__ == "__main__":
    main()
