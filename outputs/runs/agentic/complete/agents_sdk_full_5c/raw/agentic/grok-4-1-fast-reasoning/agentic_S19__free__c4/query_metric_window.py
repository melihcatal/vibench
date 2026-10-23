import boto3
from datetime import datetime, timedelta
from typing import List, Dict
import os
from observability_client import get_aws_region
from observability_models import create_metric_data_query, parse_datapoints

def query_metric_window(
    metric_name: str,
    window_minutes: int = 60,
    namespace: str = 'AWS/EC2',
    period: int = 300
) -> List[Dict[str, Any]]:
    region = get_aws_region()
    client = boto3.client('cloudwatch', region_name=region)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=window_minutes)
    mdq = create_metric_data_query('m1', metric_name, namespace, period=period)
    response = client.get_metric_data(
        MetricDataQueries=[mdq],
        StartTime=start_time,
        EndTime=end_time
    )
    mdr = response['MetricDataResults'][0]
    return parse_datapoints(mdr)