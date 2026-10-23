import os
from typing import Dict, List, Optional

import boto3
from botocore.client import BaseClient


def build_monitoring_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client(
        "cloudwatch",
        region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )


def get_default_window() -> int:
    return int(os.getenv("OBSERVABILITY_DEFAULT_WINDOW_MINUTES", "60"))


def normalize_dimensions(dimensions: Dict[str, str]) -> List[Dict[str, str]]:
    return [{"Name": str(k), "Value": str(v)} for k, v in sorted(dimensions.items()) if k and v is not None]
