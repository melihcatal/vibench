import boto3
from typing import List, Dict, Optional
from observability_client import parse_iso_time, get_default_region

def query_metric_window(
    namespace: str,
    metric_name: str,
    start_time: str,
    end_time: str,
    dimensions: Optional[List[Dict[str, str]]] = None,
    period: int = 300,
    statistics: List[str] = ['Average']
) -> List[Dict]:
    client = boto3.client('cloudwatch', region_name=get_default_region())
    start_dt = parse_iso_time(start_time)
    end_dt = parse_iso_time(end_time)
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_dt,
        EndTime=end_dt,
        Period=period,
        Statistics=statistics
    )
    return response['Datapoints']
