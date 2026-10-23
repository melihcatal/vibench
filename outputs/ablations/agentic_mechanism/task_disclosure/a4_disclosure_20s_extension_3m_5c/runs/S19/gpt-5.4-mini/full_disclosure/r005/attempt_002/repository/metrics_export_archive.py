import base64
import hashlib
import hmac
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from urllib.parse import quote, urlencode
import urllib.request
import urllib.error


@dataclass
class ArchiveResult:
    bucket: str
    object_key: str
    etag: Optional[str]
    version_id: Optional[str]
    url: str


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _amz_date(now: Optional[datetime] = None) -> str:
    now = now or datetime.now(timezone.utc)
    return now.strftime("%Y%m%dT%H%M%SZ")


def _date_stamp(now: Optional[datetime] = None) -> str:
    now = now or datetime.now(timezone.utc)
    return now.strftime("%Y%m%d")


def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _aws_sigv4_key(secret_key: str, date_stamp: str, region: str, service: str) -> bytes:
    k_date = _sign(("AWS4" + secret_key).encode("utf-8"), date_stamp)
    k_region = hmac.new(k_date, region.encode("utf-8"), hashlib.sha256).digest()
    k_service = hmac.new(k_region, service.encode("utf-8"), hashlib.sha256).digest()
    return hmac.new(k_service, b"aws4_request", hashlib.sha256).digest()


def _canonical_query(params: Dict[str, str]) -> str:
    return urlencode(sorted(params.items()), quote_via=quote, safe="-_.~")


def archive_metric_snapshot(
    snapshot: Dict[str, Any],
    bucket: Optional[str] = None,
    prefix: Optional[str] = None,
    object_key: Optional[str] = None,
) -> ArchiveResult:
    bucket = bucket or _env("AWS_S3_BUCKET")
    if not bucket:
        raise ValueError("AWS_S3_BUCKET is required")

    region = _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1"))
    access_key = _env("AWS_ACCESS_KEY_ID")
    secret_key = _env("AWS_SECRET_ACCESS_KEY")
    session_token = _env("AWS_SESSION_TOKEN")
    if not access_key or not secret_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are required")

    payload = json.dumps(snapshot, separators=(",", ":"), sort_keys=True).encode("utf-8")
    digest = _sha256_hex(payload)

    if not object_key:
        ts = datetime.now(timezone.utc).strftime("%Y/%m/%d/%H%M%S")
        snap_id = snapshot.get("snapshot_id") or snapshot.get("id") or digest[:16]
        base = f"metric-snapshots/{ts}-{snap_id}.json"
        object_key = f"{prefix.rstrip('/')}/{base}" if prefix else base

    host = f"{bucket}.s3.{region}.amazonaws.com" if region != "us-east-1" else f"{bucket}.s3.amazonaws.com"
    amz_date = _amz_date()
    date_stamp = _date_stamp()
    service = "s3"
    method = "PUT"
    uri = "/" + quote(object_key, safe="/-_.~")
    canonical_headers = [f"host:{host}", f"x-amz-content-sha256:{digest}", f"x-amz-date:{amz_date}"]
    headers = {
        "Host": host,
        "x-amz-content-sha256": digest,
        "x-amz-date": amz_date,
        "Content-Type": "application/json",
    }
    signed_headers = "host;x-amz-content-sha256;x-amz-date"
    if session_token:
        headers["x-amz-security-token"] = session_token
        canonical_headers.append(f"x-amz-security-token:{session_token}")
        signed_headers += ";x-amz-security-token"
    canonical_request = "\n".join([
        method,
        uri,
        "",
        "\n".join(canonical_headers) + "\n",
        signed_headers,
        digest,
    ])
    scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join([
        "AWS4-HMAC-SHA256",
        amz_date,
        scope,
        _sha256_hex(canonical_request.encode("utf-8")),
    ])
    signing_key = _aws_sigv4_key(secret_key, date_stamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    authorization = (
        f"AWS4-HMAC-SHA256 Credential={access_key}/{scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )
    headers["Authorization"] = authorization

    req = urllib.request.Request(f"https://{host}{uri}", data=payload, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            etag = resp.headers.get("ETag")
            version_id = resp.headers.get("x-amz-version-id")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"S3 archive failed: {exc.code} {exc.reason}: {body}") from exc

    url = f"s3://{bucket}/{object_key}"
    return ArchiveResult(bucket=bucket, object_key=object_key, etag=etag, version_id=version_id, url=url)


def archive_metric_snapshot_from_env(snapshot_json: str) -> Dict[str, Any]:
    snapshot = json.loads(snapshot_json)
    result = archive_metric_snapshot(snapshot)
    return {
        "bucket": result.bucket,
        "object_key": result.object_key,
        "etag": result.etag,
        "version_id": result.version_id,
        "url": result.url,
    }
