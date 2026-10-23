import boto3
import os
from datetime import datetime
from typing import List, Dict, Any
from observability_models import normalize_get_metric_data_result

def query_metric_window(
    namespace: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 60,
    stat: str = 'Average'
) -> List[Dict[str, Any]]:
    client = boto3.client('cloudwatch', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'e1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                    },
                    'Period': period,
                    'Stat': stat,
                },
                'ReturnData': True,
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )
    if 'MetricDataResults' in response and response['MetricDataResults']:
        return normalize_get_metric_data_result(response['MetricDataResults'][0])
    return []
