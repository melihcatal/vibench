from datetime import datetime
from typing import Dict, Any

from observability_client import ObservabilityClient
from observability_models import MetricQuery

def aggregate_metric_stats(query: MetricQuery, statistic: str = 'Average') -> Dict[str, Any]:
    client = ObservabilityClient()
    
    # CloudWatch get_metric_statistics expects dimensions as a list of dicts
    cloudwatch_dimensions = [{'Name': k, 'Value': v} for k, v in query.dimensions.items()]

    response = client.cloudwatch_client.get_metric_statistics(
        Namespace=query.namespace,
        MetricName=query.metric_name,
        Dimensions=cloudwatch_dimensions,
        StartTime=query.start_time,
        EndTime=query.end_time,
        Period=query.period,
        Statistics=[statistic]
    )

    return {
        "metric_name": query.metric_name,
        "statistic": statistic,
        "datapoints": response.get('Datapoints', [])
    }
