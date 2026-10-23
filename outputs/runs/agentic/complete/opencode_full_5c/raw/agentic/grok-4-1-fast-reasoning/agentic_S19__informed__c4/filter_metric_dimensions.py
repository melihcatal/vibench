from typing import List, Dict, Any
from observability_client import get_cloudwatch_client
from observability_models import Dimension


def filter_metric_dimensions(
    metric_name: str, namespace: str, dimension_filters: List[Dimension]
) -> List[Dict[str, Any]]:
    client = get_cloudwatch_client()
    response = client.list_metrics(
        Namespace=namespace, MetricName=metric_name, Dimensions=dimension_filters
    )
    return response["Metrics"]
