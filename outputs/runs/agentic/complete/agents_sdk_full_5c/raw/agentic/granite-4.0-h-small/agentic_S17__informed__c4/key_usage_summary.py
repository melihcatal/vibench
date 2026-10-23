import json
import boto3
from datetime import datetime, timedelta
from security_client import KeyManagementClient


def key_usage_summary(key_id: str, start_date: datetime = None, end_date: datetime = None) -> dict:
    """Summarize usage metrics for a given AWS KMS key.

    Uses CloudWatch metrics via boto3 to retrieve request counts, error counts,
    and throttles for the specified key. Optionally restricts the timeframe.

    Args:
        key_id (str): ARN or alias of the KMS key.
        start_date (datetime, optional): Lower bound of the time window.
        end_date (datetime, optional): Upper bound of the time window (defaults to now).

    Returns:
        dict: Summary containing metric names and aggregated values.
    """
    client = KeyManagementClient(service="aws_kms".upper()).get_client()
    cw = boto3.client('cloudwatch')

    if start_date is None:
        start_date = datetime.utcnow() - timedelta(days=7)
    if end_date is None:
        end_date = datetime.utcnow()

    period = 3600  # 1‑hour granularity
    metrics = [
        {'MetricName': 'AWS/KMS/Requests', 'Dimensions': [{'Name': 'KeyId', 'Value': key_id}]},
        {'MetricName': 'AWS/KMS/RequestsError', 'Dimensions': [{'Name': 'KeyId', 'Value': key_id}]},
        {'MetricName': 'AWS/KMS/Throttle', 'Dimensions': [{'Name': 'KeyId', 'Value': key_id}]}
    ]

    summary = {}
    for m in metrics:
        try:
            resp = cw.get_metric_statistics(
                Namespace='AWS/KMS',
                MetricName=m['MetricName'],
                Dimensions=m['Dimensions'],
                StartTime=start_date,
                EndTime=end_date,
                Period=period,
                Statistics=['Sum']
            )
            datapoints = resp.get('Datapoints', [])
            if datapoints:
                summary[m['MetricName']] = datapoints[0]['Sum']  # simple aggregation
            else:
                summary[m['MetricName']] = 0
        except Exception as exc:
            summary[m['MetricName']] = f"error: {exc}"
    return summary
