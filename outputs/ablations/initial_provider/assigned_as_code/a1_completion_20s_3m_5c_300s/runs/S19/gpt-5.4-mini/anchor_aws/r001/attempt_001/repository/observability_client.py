from dataclasses import dataclass
import os

import boto3


@dataclass
class ObservabilityConfig:
    region: str | None
    namespace: str
    period_seconds: int
    dimensions: dict
    bucket: str | None
    key_prefix: str
    locale: str


def load_config(config=None):
    merged = dict(config or {})
    return ObservabilityConfig(
        region=merged.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        namespace=merged.get("namespace") or os.environ.get("CLOUDWATCH_NAMESPACE", "ManagedMetrics"),
        period_seconds=int(merged.get("period_seconds", os.environ.get("METRICS_PERIOD_SECONDS", 60))),
        dimensions=dict(merged.get("dimensions", {})),
        bucket=merged.get("bucket") or os.environ.get("METRICS_ARCHIVE_BUCKET"),
        key_prefix=merged.get("key_prefix") or os.environ.get("METRICS_ARCHIVE_PREFIX", "archives/"),
        locale=merged.get("locale") or os.environ.get("TARGET_LOCALE", "en"),
    )


def cloudwatch_client(config=None):
    cfg = load_config(config)
    return boto3.client("cloudwatch", region_name=cfg.region)


def s3_client(config=None):
    cfg = load_config(config)
    return boto3.client("s3", region_name=cfg.region)
