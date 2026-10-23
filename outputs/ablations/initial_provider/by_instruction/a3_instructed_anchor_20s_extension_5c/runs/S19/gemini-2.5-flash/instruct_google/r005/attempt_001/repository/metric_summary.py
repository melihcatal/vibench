import datetime
import os
from typing import Dict, Any, List, Optional

import boto3

# Helper imports (though not directly used by CloudWatch, maintaining structure)
from observability_models import MetricDataPoint, MetricQueryResult

def summarize_metric_trends(
    namespace: str,
    metric_name: str,
    dimensions: List[Dict[str, str]],
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int = 300,  # 5 minutes in seconds
    statistic: str = 'Average'
) -> Dict[str, Any]:
    cloudwatch = boto3.client('cloudwatch')

    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=[statistic],
        Unit='Count' # Example unit, would be dynamic based on metric
    )

    summary_data = {
        "metric_name": metric_name,
        "namespace": namespace,
        "dimensions": dimensions,
        "statistic": statistic,
        "datapoints": []
    }

    for dp in response.get('Datapoints', []):
        summary_data["datapoints"].append({
            "timestamp": dp['Timestamp'].isoformat(),
            "value": dp[statistic],
            "unit": dp['Unit']
        })

    return summary_data
