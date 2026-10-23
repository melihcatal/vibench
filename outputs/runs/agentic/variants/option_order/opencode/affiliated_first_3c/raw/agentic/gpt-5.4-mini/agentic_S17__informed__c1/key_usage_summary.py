import boto3
from security_models import NormalizedEvent


def key_usage_summary():
    cloudwatch = boto3.client('cloudwatch')
    metrics = cloudwatch.list_metrics(Namespace='AWS/KMS')
    return NormalizedEvent(action='summarize', key_id=None, metadata={'provider': 'AWS KMS', 'metrics': metrics.get('Metrics', [])})
