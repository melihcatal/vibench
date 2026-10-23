import boto3
from datetime import datetime, timedelta
from typing import Dict
import os

def key_usage_summary(key_id: str, lookback_hours: int = 24) -> Dict[str, Dict[str, float]]:
    region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    cw_client = boto3.client('cloudwatch', region_name=region)
    end = datetime.utcnow()
    start = end - timedelta(hours=lookback_hours)
    metrics = ['NumberOfRequests', 'BytesEncrypted', 'BytesDecrypted']
    summary = {}
    for metric_name in metrics:
        resp = cw_client.get_metric_statistics(
            Namespace='AWS/KMS',
            MetricName=metric_name,
            StartTime=start,
            EndTime=end,
            Period=300,
            Statistics=['Sum', 'Average']
        )
        datapoints = resp.get('Datapoints', [])
        total = sum(dp.get('Sum', 0.0) for dp in datapoints)
        avg = sum(dp.get('Average', 0.0) for dp in datapoints) / max(1, len(datapoints))
        summary[metric_name] = {'total': total, 'average': avg}
    return summary