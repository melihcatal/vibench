import boto3

from security_models import KeyUsageSummary, response_map


def key_usage_summary(key_id: str):
    cloudwatch = boto3.client('cloudwatch')
    metrics = cloudwatch.list_metrics(Namespace='AWS/KMS', MetricName='CustomerMasterKeyUsage')
    return response_map(key_id=key_id, event_count=len(metrics.get('Metrics', [])), event_type='CustomerMasterKeyUsage')
