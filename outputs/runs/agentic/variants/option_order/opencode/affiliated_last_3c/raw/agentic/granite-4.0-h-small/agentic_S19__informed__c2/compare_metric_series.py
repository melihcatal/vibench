# [SAME-SCENARIO] compare_metric_series.py

# Compare metric values for two resources or dimension filters over the same window.
# Provider: Amazon CloudWatch Metrics (boto3 SDK)

import os
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any

from .query_metric_window import query_metric_window


def compare_metric_series(
    metric_name: str,
    resource_a: str,
    resource_b: str,
    window_minutes: int = 60,
    period: int = 60,
    dimensions_a: List[Dict[str, Any]] = None,
    dimensions_b: List[Dict[str, Any]] = None,
    statistics: List[str] = ["Average"],
) -> Tuple[List[Any], List[Any]]:
    """
    Queries the same *metric_name* for two distinct resources defined via *dimensions*.
    Returns a tuple of two lists: (data_a, data_b) where each list contains
    the datapoints corresponding to its dimensions.

    Example dimensions format:
        [{'InstanceId': 'i-0abc123'}]
    """
    end = datetime.utcnow()
    start = end - timedelta(minutes=window_minutes)
    data_a = (
        query_metric_window(
            metric_name=metric_name,
            namespace="AWS/EC2",
            window_minutes=window_minutes,
            period=period,
            statistics=statistics,
        )
        if dimensions_a is None
        else query_metric_window(
            metric_name=metric_name,
            namespace="AWS/EC2",
            window_minutes=window_minutes,
            period=period,
            statistics=statistics,
            dimensions=dimensions_a,
        )
    )
    data_b = (
        query_metric_window(
            metric_name=metric_name,
            namespace="AWS/EC2",
            window_minutes=window_minutes,
            period=period,
            statistics=statistics,
        )
        if dimensions_b is None
        else query_metric_window(
            metric_name=metric_name,
            namespace="AWS/EC2",
            window_minutes=window_minutes,
            period=period,
            statistics=statistics,
            dimensions=dimensions_b,
        )
    )
    return data_a, data_b
