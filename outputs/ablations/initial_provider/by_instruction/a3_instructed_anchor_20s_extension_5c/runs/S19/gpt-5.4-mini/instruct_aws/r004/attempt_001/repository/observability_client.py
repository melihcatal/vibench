import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import boto3

from observability_models import MetricWindowRequest, normalize_dimensions


def load_observability_config() -> Dict[str, Any]:
    return {
        "region_name": os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1",
        "namespace": os.getenv("OBSERVABILITY_NAMESPACE", "AWS/EC2"),
        "metric_name": os.getenv("OBSERVABILITY_METRIC_NAME", "CPUUtilization"),
    }


def cloudwatch_client():
    return boto3.client("cloudwatch", region_name=load_observability_config()["region_name"])


def metric_query_from_request(request: MetricWindowRequest, query_id: str = "m1") -> Dict[str, Any]:
    return {
        "Id": query_id,
        "MetricStat": {
            "Metric": {
                "Namespace": request.namespace,
                "MetricName": request.metric_name,
                "Dimensions": normalize_dimensions(request.dimensions),
            },
            "Period": request.period,
            "Stat": request.statistics[0],
            **({"Unit": request.unit} if request.unit else {}),
        },
        "ReturnData": True,
    }


def get_metric_data(request: MetricWindowRequest, client: Optional[Any] = None) -> Dict[str, Any]:
    cw = client or cloudwatch_client()
    query = metric_query_from_request(request)
    response = cw.get_metric_data(
        MetricDataQueries=[query],
        StartTime=request.start_time,
        EndTime=request.end_time,
        ScanBy="TimestampDescending",
    )
    return response


def list_metric_series(namespace: str, metric_name: str, dimensions: Optional[Dict[str, str]] = None, client: Optional[Any] = None) -> List[Dict[str, Any]]:
    cw = client or cloudwatch_client()
    response = cw.list_metrics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=normalize_dimensions(dimensions),
    )
    return response.get("Metrics", [])
