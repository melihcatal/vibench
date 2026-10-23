import boto3
import os
from datetime import datetime, timedelta
from typing import Dict, Any

def key_usage_summary(key_id: str, hours: int = 24) -> Dict[str, Any]:
    region = os.getenv('AWS_REGION', 'us-east-1')
    cw_client = boto3.client('cloudwatch', region_name=region)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    response = cw_client.get_metric_statistics(
        Namespace='AWS/KMS',
        MetricName='NumberOfRequests',
        Dimensions=[
            {
                'Name': 'KeyId',
                'Value': key_id
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Sum', 'Average']
    )
    return {
        'key_id': key_id,
        'summary': response.get('Datapoints', [])
    }
