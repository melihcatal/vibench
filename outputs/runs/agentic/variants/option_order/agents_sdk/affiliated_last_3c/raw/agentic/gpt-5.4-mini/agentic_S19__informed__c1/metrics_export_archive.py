from __future__ import annotations

from observability_client import client


def metrics_export_archive(bucket: str, key: str, content: str):
    return client().export_snapshot(bucket=bucket, key=key, content=content)
