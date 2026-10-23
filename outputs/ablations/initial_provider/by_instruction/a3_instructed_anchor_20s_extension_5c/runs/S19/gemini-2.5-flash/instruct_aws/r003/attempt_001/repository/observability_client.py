import boto3
from typing import Dict, Any, List
from datetime import datetime, timedelta

class ObservabilityClient:
    def __init__(self):
        self.cloudwatch_client = boto3.client('cloudwatch')

    def query_metric_data(self, namespace: str, metric_name: str, dimensions: Dict[str, str], 
                            start_time: datetime, end_time: datetime, period: int) -> List[Dict[str, Any]]:
        response = self.cloudwatch_client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'm1',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': namespace,
                            'MetricName': metric_name,
                            'Dimensions': [{
                                'Name': k,
                                'Value': v
                            } for k, v in dimensions.items()]
                        },
                        'Period': period,
                        'Stat': 'Average' # Can be customized based on need
                    },
                    'ReturnData': True,
                },
            ],
            StartTime=start_time,
            EndTime=end_time
        )
        return response.get('MetricDataResults', [])
