from datetime import datetime, timedelta
from typing import Dict, Any
from observability_client import ObservabilityClient
from observability_models import MetricQueryRequest

def aggregate_metric_stats(request: MetricQueryRequest, statistic: str = "Average") -> Dict[str, Any]:
    client = ObservabilityClient()

    dimensions_list = []
    if request.dimensions:
        for name, value in request.dimensions.items():
            dimensions_list.append({"Name": name, "Value": value})

    response = client.cloudwatch_client.get_metric_statistics(
        Namespace="CustomMetrics",  # Replace with actual namespace
        MetricName=request.metric_name,
        Dimensions=dimensions_list,
        StartTime=datetime.fromisoformat(request.start_time).timestamp(),
        EndTime=datetime.fromisoformat(request.end_time).timestamp(),
        Period=300,  # 5 minutes in seconds
        Statistics=[statistic]
    )

    return response.get("Datapoints", [])
