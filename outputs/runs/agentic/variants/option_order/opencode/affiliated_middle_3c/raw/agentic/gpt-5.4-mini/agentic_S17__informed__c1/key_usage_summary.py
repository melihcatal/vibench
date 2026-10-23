import boto3
from security_client import get_region_name
from security_models import normalize_message

def key_usage_summary(key_id: str, days: int = 7) -> dict:
    client = boto3.client('cloudwatch', region_name=get_region_name())
    metric = client.get_metric_statistics(Namespace='AWS/KMS', MetricName='CustomerMasterKeyUsage', Dimensions=[{'Name': 'KeyId', 'Value': normalize_message(key_id)}], StartTime=__import__('datetime').datetime.utcnow() - __import__('datetime').timedelta(days=days), EndTime=__import__('datetime').datetime.utcnow(), Period=86400, Statistics=['Sum'])
    return {'provider': 'aws_kms', 'key_id': key_id, 'points': metric.get('Datapoints', [])}
