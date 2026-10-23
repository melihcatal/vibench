# key_usage_summary.py
import os
from typing import List, Dict, Any

from security_client import SecurityClient

# AWS KMS (later-step) - usage summary


def get_key_usage(key_id: str) -> Dict[str, Any]:
    """Retrieve a simplified usage summary for a KMS key using AWS CloudWatch metrics."""
    client = SecurityClient()
    # The CloudWatch client is used here; credentials are inherited from env.
    cw = boto3.client("cloudwatch")
    # Query the KMS metric without specific dimensions; returns count of API calls.
    response = cw.get_metric_statistics(
        Namespace="AWS/KMS",
        MetricName="APIActivity",
        Dimensions=[{"Name": "KeyId", "Value": key_id}],
        StartTime=(datetime.utcnow() - timedelta(days=7)),
        EndTime=datetime.utcnow(),
        Period=86400,
        Statistics=["Sum"],
    )
    # Simplify to total calls in the period
    total_calls = response["Datapoints"][-1]["Sum"] if response["Datapoints"] else 0
    return {
        "key_id": key_id,
        "service": "AWS KMS",
        "metric": "Total API Calls",
        "value": int(total_calls),
    }


def summarize_usage(key_ids: List[str]) -> List[Dict[str, Any]]:
    """Summarize usage for a list of keys."""
    summary = []
    for k in key_ids:
        summary.append(get_key_usage(k))
    return summary
