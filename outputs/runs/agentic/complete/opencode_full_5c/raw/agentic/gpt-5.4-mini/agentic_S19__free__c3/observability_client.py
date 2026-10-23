import os
from typing import Any, Dict, Optional

import boto3
from botocore.client import BaseClient


def _region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_cloudwatch_client() -> BaseClient:
    return boto3.client("cloudwatch", region_name=_region())


def get_s3_client() -> BaseClient:
    return boto3.client("s3", region_name=_region())


def get_translate_client() -> BaseClient:
    return boto3.client("translate", region_name=_region())


def get_comprehend_client() -> BaseClient:
    return boto3.client("comprehend", region_name=_region())


def cloudwatch_metric_data(
    metric_name: str,
    start_time: str,
    end_time: str,
    period: int = 60,
    dimensions: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        "MetricDataQueries": [
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {
                        "Namespace": os.getenv(
                            "OBSERVABILITY_NAMESPACE", "ManagedMetrics"
                        ),
                        "MetricName": metric_name,
                        "Dimensions": [
                            {"Name": k, "Value": v}
                            for k, v in (dimensions or {}).items()
                        ],
                    },
                    "Period": period,
                    "Stat": "Average",
                },
                "ReturnData": True,
            }
        ],
        "StartTime": start_time,
        "EndTime": end_time,
    }
    return get_cloudwatch_client().get_metric_data(**params)
