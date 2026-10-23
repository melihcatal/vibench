import os
import json
import base64
import hashlib
from typing import Any, Dict, Optional
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


DATADOG_API_KEY = os.environ.get("DATADOG_API_KEY", "")
DATADOG_APP_KEY = os.environ.get("DATADOG_APP_KEY", "")
DATADOG_SITE = os.environ.get("DATADOG_SITE", "datadoghq.com")
DATADOG_API_BASE = f"https://api.{DATADOG_SITE}"

PERSPECTIVE_API_KEY = os.environ.get("GOOGLE_PERSPECTIVE_API_KEY", "")
PERSPECTIVE_API_BASE = "https://commentanalyzer.googleapis.com"

DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY", "")
DEEPL_API_BASE = "https://api-free.deepl.com"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "metrics-archive")


def _create_retry_session(
    retries: int = 3,
    backoff_factor: float = 0.5,
    status_forcelist: Optional[list] = None,
) -> requests.Session:
    if status_forcelist is None:
        status_forcelist = [429, 500, 502, 503, 504]
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=["GET", "POST", "PUT", "DELETE"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session


def create_datadog_session() -> requests.Session:
    session = _create_retry_session()
    session.headers.update(
        {
            "DD-API-KEY": DATADOG_API_KEY,
            "DD-APPLICATION-KEY": DATADOG_APP_KEY,
            "Content-Type": "application/json",
        }
    )
    return session


def create_perspective_session() -> requests.Session:
    session = _create_retry_session()
    session.headers.update(
        {
            "Content-Type": "application/json",
        }
    )
    return session


def create_deepl_session() -> requests.Session:
    session = _create_retry_session()
    session.headers.update(
        {
            "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
    )
    return session


def create_s3_session() -> requests.Session:
    return _create_retry_session()


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {
        "datadog_api_key": DATADOG_API_KEY,
        "datadog_app_key": DATADOG_APP_KEY,
        "datadog_site": DATADOG_SITE,
        "perspective_api_key": PERSPECTIVE_API_KEY,
        "deepl_api_key": DEEPL_API_KEY,
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "aws_region": AWS_REGION,
        "s3_bucket_name": S3_BUCKET_NAME,
    }


def validate_datadog_credentials() -> bool:
    return bool(DATADOG_API_KEY) and bool(DATADOG_APP_KEY)


def validate_perspective_credentials() -> bool:
    return bool(PERSPECTIVE_API_KEY)


def validate_deepl_credentials() -> bool:
    return bool(DEEPL_API_KEY)


def validate_s3_credentials() -> bool:
    return bool(AWS_ACCESS_KEY_ID) and bool(AWS_SECRET_ACCESS_KEY)


def compute_checksum(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def serialize_metric_data(data: Any) -> bytes:
    if hasattr(data, "__dict__"):
        data = data.__dict__
    return json.dumps(data, default=str, indent=2).encode("utf-8")


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso_timestamp(ts: str) -> datetime:
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)
