import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional

import requests

from observability_client import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
    S3_BUCKET_NAME,
    compute_checksum,
    create_datadog_session,
    create_s3_session,
    serialize_metric_data,
    validate_datadog_credentials,
    validate_s3_credentials,
)
from observability_models import (
    MetricDataPoint,
    MetricExportArchive,
    MetricQueryRequest,
    normalize_datadog_response,
)


def _sign_request(
    method: str,
    url: str,
    headers: Dict[str, str],
    body: bytes,
    access_key: str,
    secret_key: str,
    region: str,
    service: str = "s3",
) -> Dict[str, str]:
    import hmac
    from datetime import datetime as dt
    from hashlib import sha256

    now = dt.utcnow()
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")

    payload_hash = sha256(body).hexdigest()
    headers["x-amz-date"] = amz_date
    headers["x-amz-content-sha256"] = payload_hash
    headers["host"] = url.split("//")[1].split("/")[0]

    canonical_uri = "/" + "/".join(url.split("//")[1].split("/")[1:])
    canonical_querystring = ""
    canonical_headers = (
        "\n".join(
            f"{k.lower()}:{v}"
            for k, v in sorted(headers.items())
            if k.lower()
            in ("host", "x-amz-date", "x-amz-content-sha256", "content-type")
        )
        + "\n"
    )
    signed_headers = ";".join(
        k.lower()
        for k in sorted(headers.keys())
        if k.lower() in ("host", "x-amz-date", "x-amz-content-sha256", "content-type")
    )

    canonical_request = "\n".join(
        [
            method,
            canonical_uri,
            canonical_querystring,
            canonical_headers,
            signed_headers,
            payload_hash,
        ]
    )

    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join(
        [
            algorithm,
            amz_date,
            credential_scope,
            sha256(canonical_request.encode("utf-8")).hexdigest(),
        ]
    )

    signing_key = _get_signature_key(secret_key, date_stamp, region, service)
    signature = hmac.new(
        signing_key, string_to_sign.encode("utf-8"), sha256
    ).hexdigest()

    authorization = (
        f"{algorithm} "
        f"Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, "
        f"Signature={signature}"
    )
    headers["Authorization"] = authorization

    return headers


def _get_signature_key(key: str, date_stamp: str, region: str, service: str) -> bytes:
    import hmac
    from hashlib import sha256

    def sign(msg: bytes, data: str) -> bytes:
        return hmac.new(msg, data.encode("utf-8"), sha256).digest()

    k_date = sign(("AWS4" + key).encode("utf-8"), date_stamp)
    k_region = sign(k_date, region)
    k_service = sign(k_region, service)
    k_signing = sign(k_service, "aws4_request")
    return k_signing


def _fetch_metric_data(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    aggregation: str = "avg",
    dimensions: Optional[Dict[str, str]] = None,
) -> List[MetricDataPoint]:
    query = f"{aggregation}:{metric_name}"
    if dimensions:
        dim_parts = []
        for k, v in dimensions.items():
            dim_parts.append(f"{k}:{v}")
        query = f"{query}{{{' AND '.join(dim_parts)}}}"

    payload = {
        "query": query,
        "from": int(start_time.timestamp()),
        "to": int(end_time.timestamp()),
    }

    session = create_datadog_session()
    api_url = "https://api.datadoghq.com/api/v1/query"

    response = session.get(api_url, params=payload, timeout=30)
    response.raise_for_status()

    raw_data = response.json()
    return normalize_datadog_response(raw_data)


def metrics_export_archive(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    aggregation: str = "avg",
    dimensions: Optional[Dict[str, str]] = None,
    bucket_name: Optional[str] = None,
    archive_prefix: str = "metrics-archive",
) -> MetricExportArchive:
    if not validate_datadog_credentials():
        raise ValueError(
            "Datadog credentials not configured. Set DATADOG_API_KEY and DATADOG_APP_KEY environment variables."
        )

    if not validate_s3_credentials():
        raise ValueError(
            "AWS S3 credentials not configured. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    data_points = _fetch_metric_data(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        aggregation=aggregation,
        dimensions=dimensions,
    )

    archive_data = {
        "metric_name": metric_name,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat,
        "aggregation": aggregation,
        "dimensions": dimensions or {},
        "data_points": [
            {
                "timestamp": dp.timestamp.isoformat(),
                "value": dp.value,
                "dimensions": dp.dimensions,
                "resource_id": dp.resource_id,
            }
            for dp in data_points
        ],
    }

    serialized = serialize_metric_data(archive_data)
    checksum = compute_checksum(serialized)

    target_bucket = bucket_name or S3_BUCKET_NAME
    timestamp_str = start_time.strftime("%Y%m%dT%H%M%S")
    object_key = f"{archive_prefix}/{metric_name}/{timestamp_str}/{checksum}.json"

    s3_url = f"https://{target_bucket}.s3.{AWS_REGION}.amazonaws.com/{object_key}"

    session = create_s3_session()
    headers = {
        "Content-Type": "application/json",
        "x-amz-storage-class": "STANDARD_IA",
    }

    signed_headers = _sign_request(
        method="PUT",
        url=s3_url,
        headers=headers,
        body=serialized,
        access_key=AWS_ACCESS_KEY_ID,
        secret_key=AWS_SECRET_ACCESS_KEY,
        region=AWS_REGION,
        service="s3",
    )

    response = session.put(
        s3_url,
        data=serialized,
        headers=signed_headers,
        timeout=60,
    )
    response.raise_for_status()

    archive_url = f"https://s3.{AWS_REGION}.amazonaws.com/{target_bucket}/{object_key}"

    return MetricExportArchive(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        data_points=data_points,
        archive_key=object_key,
        archive_url=archive_url,
        archived_at=datetime.utcnow(),
        checksum=checksum,
    )
