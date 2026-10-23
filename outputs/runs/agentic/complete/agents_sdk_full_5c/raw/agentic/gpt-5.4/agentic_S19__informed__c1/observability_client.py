from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, Iterable, List, Optional

import boto3
from botocore.config import Config

from observability_models import ensure_utc


DEFAULT_CLOUDWATCH_NAMESPACE = os.getenv("CLOUDWATCH_NAMESPACE", "AWS/EC2")
DEFAULT_CLOUDWATCH_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


class CloudWatchObservabilityClient:
    def __init__(self, region_name: Optional[str] = None) -> None:
        self.region_name = region_name or DEFAULT_CLOUDWATCH_REGION
        self.client = boto3.client(
            "cloudwatch",
            region_name=self.region_name,
            config=Config(retries={"max_attempts": 5, "mode": "standard"}),
        )

    @staticmethod
    def _build_dimensions(dimensions: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
        dimensions = dimensions or {}
        return [{"Name": key, "Value": value} for key, value in dimensions.items()]

    def get_metric_statistics(
        self,
        *,
        namespace: str,
        metric_name: str,
        start_time: datetime,
        end_time: datetime,
        period: int,
        statistics: Iterable[str],
        dimensions: Optional[Dict[str, str]] = None,
    ) -> Dict:
        return self.client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            StartTime=ensure_utc(start_time),
            EndTime=ensure_utc(end_time),
            Period=period,
            Statistics=list(statistics),
            Dimensions=self._build_dimensions(dimensions),
        )



def get_cloudwatch_client(region_name: Optional[str] = None) -> CloudWatchObservabilityClient:
    return CloudWatchObservabilityClient(region_name=region_name)
