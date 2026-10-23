import boto3
from datetime import datetime, timedelta
from typing import Dict, Any
from security_client import get_aws_region, get_encrypt_key_id

def summarize_key_usage(key_id: str = None, hours: int = 24) -> Dict[str, Any]:
    if key_id is None:
        key_id = get_encrypt_key_id()
    region = get_aws_region()
    kms_client = boto3.client('kms', region_name=region)
    cw_client = boto3.client('cloudwatch', region_name=region)

    key_desc = kms_client.describe_key(KeyId=key_id)
    metadata = key_desc['KeyMetadata']

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    def get_metric_sum(metric_name: str) -> float:
        resp = cw_client.get_metric_statistics(
            Namespace='AWS/KMS',
            MetricName=metric_name,
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=['Sum']
        )
        if resp['Datapoints']:
            return resp['Datapoints'][0]['Sum'] or 0.0
        return 0.0

    summary = {
        'key_arn': metadata['Arn'],
        'key_state': metadata['KeyState'],
        'enabled': metadata['Enabled'],
        'key_usage': metadata['KeyUsage'],
        'creation_date': metadata['CreationDate'].isoformat(),
        'description': metadata.get('Description', ''),
        'requests_last_hours': get_metric_sum('NumberOfRequests'),
        'bytes_encrypted': get_metric_sum('BytesEncrypted'),
        'bytes_decrypted': get_metric_sum('BytesDecrypted'),
    }
    return summary