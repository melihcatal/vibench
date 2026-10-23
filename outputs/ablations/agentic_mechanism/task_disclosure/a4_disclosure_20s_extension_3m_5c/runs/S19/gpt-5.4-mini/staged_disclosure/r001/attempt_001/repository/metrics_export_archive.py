import argparse
import gzip
import hashlib
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class S3ArchiveConfig:
    bucket: str
    region_name: Optional[str] = None
    prefix: str = "metric-snapshots"
    retention_days: int = 30

    @classmethod
    def from_env(cls) -> "S3ArchiveConfig":
        bucket = os.getenv("AWS_S3_ARCHIVE_BUCKET")
        if not bucket:
            raise ValueError("Missing AWS_S3_ARCHIVE_BUCKET")
        region_name = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
        prefix = os.getenv("AWS_S3_ARCHIVE_PREFIX", "metric-snapshots")
        retention_days = int(os.getenv("METRIC_ARCHIVE_RETENTION_DAYS", "30"))
        return cls(bucket=bucket, region_name=region_name, prefix=prefix.strip("/"), retention_days=retention_days)


class MetricsExportArchiver:
    def __init__(self, config: Optional[S3ArchiveConfig] = None):
        self.config = config or S3ArchiveConfig.from_env()
        self._client = boto3.client("s3", region_name=self.config.region_name)

    @staticmethod
    def _iter_snapshot_files(source_dir: Path) -> Iterable[Path]:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file() and not path.name.startswith("."):
                yield path

    @staticmethod
    def _archive_name(source_file: Path) -> str:
        stamp = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        digest = hashlib.sha256(source_file.read_bytes()).hexdigest()[:12]
        return f"{source_file.stem}-{stamp}-{digest}.json.gz"

    def _object_key(self, source_file: Path) -> str:
        return f"{self.config.prefix}/{source_file.parent.name}/{self._archive_name(source_file)}"

    def archive_file(self, source_file: Path) -> str:
        data = source_file.read_bytes()
        compressed = gzip.compress(data)
        key = self._object_key(source_file)
        self._client.put_object(
            Bucket=self.config.bucket,
            Key=key,
            Body=compressed,
            ContentType="application/gzip",
            Metadata={
                "source-file": source_file.name,
                "source-bytes": str(len(data)),
                "archived-at": datetime.now(tz=timezone.utc).isoformat(),
            },
        )
        return key

    def archive_directory(self, source_dir: Path) -> list[str]:
        archived: list[str] = []
        for source_file in self._iter_snapshot_files(source_dir):
            archived.append(self.archive_file(source_file))
        return archived

    def enforce_retention(self) -> int:
        if self.config.retention_days <= 0:
            return 0
        cutoff = datetime.now(tz=timezone.utc).timestamp() - (self.config.retention_days * 86400)
        deleted = 0
        paginator = self._client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.config.bucket, Prefix=f"{self.config.prefix}/"):
            for obj in page.get("Contents", []):
                if obj["LastModified"].timestamp() < cutoff:
                    self._client.delete_object(Bucket=self.config.bucket, Key=obj["Key"])
                    deleted += 1
        return deleted


def main() -> None:
    parser = argparse.ArgumentParser(description="Archive exported metric snapshots to Amazon S3")
    parser.add_argument("source_dir", nargs="?", default=".")
    parser.add_argument("--retention-days", type=int, default=None)
    args = parser.parse_args()
    config = S3ArchiveConfig.from_env()
    if args.retention_days is not None:
        config = S3ArchiveConfig(bucket=config.bucket, region_name=config.region_name, prefix=config.prefix, retention_days=args.retention_days)
    archiver = MetricsExportArchiver(config)
    archiver.archive_directory(Path(args.source_dir))
    archiver.enforce_retention()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, ClientError, BotoCoreError) as exc:
        raise SystemExit(str(exc))
