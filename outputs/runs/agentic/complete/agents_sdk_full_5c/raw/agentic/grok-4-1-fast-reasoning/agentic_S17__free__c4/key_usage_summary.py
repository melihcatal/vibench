import boto3
import datetime
from typing import Dict

def key_usage_summary(key_id: str, period_hours: int = 24) -> Dict[str, float]:
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(hours=period_hours)
    cw_client = boto3.client('cloudwatch')
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
    datapoints = response.get('Datapoints', [])
    total_requests = sum(dp.get('Sum', 0) or 0 for dp in datapoints)
    avg_requests = sum(dp.get('Average', 0) or 0 for dp in datapoints) / max(len(datapoints), 1)
    return {
        'total_requests': total_requests,
        'average_requests_per_hour': avg_requests
    }