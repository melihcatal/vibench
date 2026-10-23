from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests


def metrics_export_archive(
    snapshot: Dict[str, Any],
    object_name: str,
    content_type: str = "application/json",
    session: Optional[requests.Session] = None,
) -> Dict[str, Any]:
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    bucket_name = os.environ.get("CLOUDFLARE_R2_BUCKET")
    access_key_id = os.environ.get("CLOUDFLARE_R2_ACCESS_KEY_ID")
    secret_access_key = os.environ.get("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
    if not account_id or not bucket_name or not access_key_id or not secret_access_key:
        raise ValueError("Missing Cloudflare R2 configuration")
    http = session or requests.Session()
    endpoint = (
        f"https://{account_id}.r2.cloudflarestorage.com/{bucket_name}/{object_name}"
    )
    body = json.dumps(
        {
            "archived_at": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "snapshot": snapshot,
        }
    ).encode("utf-8")
    response = http.put(
        endpoint,
        data=body,
        headers={
            "Content-Type": content_type,
            "x-amz-content-sha256": "UNSIGNED-PAYLOAD",
            "x-amz-date": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        },
        auth=(access_key_id, secret_access_key),
        timeout=60,
    )
    response.raise_for_status()
    return {
        "provider": "Cloudflare R2",
        "bucket": bucket_name,
        "object_name": object_name,
        "endpoint": endpoint,
        "status_code": response.status_code,
    }
