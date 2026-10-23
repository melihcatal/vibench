from typing import Dict, List, Optional
import os
import boto3
from datetime import datetime, timedelta


class CloudWatchMetricsAggregator:
    def __init__(self):
        self.client = boto3.client(
            "cloudwatch",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def aggregate_metric_stats(
        self,
        metric_name: str,
        namespace: str,
        start_time: datetime,
        end_time: datetime,
        dimensions: Optional[List[Dict[str, str]]] = None,
    ) -> Dict:
        response = self.client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions or [],
            StartTime=start_time,
            EndTime=end_time,
            Period=int((end_time - start_time).total_seconds()),
            Statistics=["Average", "Sum", "Minimum", "Maximum"],
        )
        datapoints = response.get("Datapoints", [])
        if not datapoints:
            return {}
        latest_datapoint = max(datapoints, key=lambda x: x["Timestamp"])
        return {
            "metric": metric_name,
            "namespace": namespace,
            "timestamp": latest_datapoint["Timestamp"],
            "average": latest_datapoint.get("Average"),
            "sum": latest_datapoint.get("Sum"),
            "minimum": latest_datapoint.get("Minimum"),
            "maximum": latest_datapoint.get("Maximum"),
        }
