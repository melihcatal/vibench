import os
from typing import Dict, List, Optional, Union
import boto3
from botocore.client import BaseClient
from datetime import datetime


class ObservabilityClient:
    """
    Local configuration and client helper utilities for Amazon CloudWatch Metrics.
    """

    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.cloudwatch_client = self._create_cloudwatch_client()

    def _create_cloudwatch_client(self) -> BaseClient:
        """Create and return a CloudWatch client."""
        return boto3.client(
            "cloudwatch",
            region_name=self.region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def get_metric_data(
        self,
        metric_name: str,
        namespace: str,
        start_time: datetime,
        end_time: datetime,
        dimensions: Optional[List[Dict[str, str]]] = None,
        statistics: List[str] = None,
    ) -> Dict:
        """
        Query metric data from CloudWatch.

        Args:
            metric_name: Name of the CloudWatch metric.
            namespace: Namespace of the CloudWatch metric.
            start_time: Start of the time window.
            end_time: End of the time window.
            dimensions: Optional list of dimension dictionaries.
            statistics: List of statistics to retrieve (e.g., ["Average", "Sum"]).

        Returns:
            Response from CloudWatch get_metric_statistics API.
        """
        if dimensions is None:
            dimensions = []
        if statistics is None:
            statistics = ["Average"]

        return self.cloudwatch_client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=int((end_time - start_time).total_seconds()),
            Statistics=statistics,
        )


def load_observability_config() -> Dict[str, Union[str, bool]]:
    """
    Load configuration for Amazon CloudWatch Metrics from environment variables.

    Returns:
        Dictionary containing configuration values.
    """
    return {
        "region": os.getenv("AWS_REGION", "us-east-1"),
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "use_ssl": os.getenv("AWS_USE_SSL", "true").lower() == "true",
    }
