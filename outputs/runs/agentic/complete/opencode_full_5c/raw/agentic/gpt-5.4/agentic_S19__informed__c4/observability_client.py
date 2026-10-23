from __future__ import annotations

import os
from typing import Dict, Optional

import boto3

from observability_models import MetricWindowRequest


def get_cloudwatch_client(region_name: Optional[str] = None):
    return boto3.client(
        "cloudwatch",
        region_name=region_name
        or os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    )


def build_get_metric_statistics_params(
    request: MetricWindowRequest,
) -> Dict[str, object]:
    params: Dict[str, object] = {
        "Namespace": request.namespace,
        "MetricName": request.metric,
        "Dimensions": [
            {"Name": name, "Value": value} for name, value in request.dimensions.items()
        ],
        "StartTime": request.start_iso(),
        "EndTime": request.end_iso(),
        "Period": request.period,
        "Statistics": [request.stat],
    }
    if request.unit:
        params["Unit"] = request.unit
    return params
