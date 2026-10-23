import boto3
from datetime import datetime, timedelta
from typing import Dict

def key_usage_summary(key_id: str, days_back: int = 1) -> Dict[str, float]:
    cw_client = boto3.client('cloudwatch')
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days_back)
    
    metrics = ['BytesEncrypted', 'NumberOfRequests']
    summary = {}
    
    for metric_name in metrics:
        response = cw_client.get_metric_statistics(
            Namespace='AWS/KMS',
            MetricName=metric_name,
            Dimensions=[
                {
                    'Name': 'KeyId',
                    'Value': key_id
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=['Sum']
        )
        total = sum(dp.get('Sum', 0) or 0 for dp in response.get('Datapoints', []))
        summary[f'{metric_name}_total'] = total
    
    return summary