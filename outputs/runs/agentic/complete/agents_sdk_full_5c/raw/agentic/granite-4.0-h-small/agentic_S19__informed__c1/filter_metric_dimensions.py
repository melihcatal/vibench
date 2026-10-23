# SAME-SCENARIO: filter_metric_dimensions.py
from observability_client import MetricsClient
from observability_models import FilteredMetricQuery, DimensionFilter

def filter_metric_dimensions(metric_name: str, filter_expression: str, start: str, end: str):
    # Example filter using resource labels: resource.label.zone='us-central1-a' AND metric.label.instance_id='instance-1'
    # Here we construct a simple expression based on dimension keys/values.
    dimensions = []
    for part in filter_expression.split(' AND '):
        key, val = part.split('=', 1)
        dimensions.append(DimensionFilter(name=key.strip(), value=val.strip().strip('"')))
    query = FilteredMetricQuery(metric=metric_name, filter=dimensions, start=start, end=end)
    return MetricsClient.get().query(query)

if __name__ == "__main__":
    # Using IBM Cloud Monitoring (set IBM_CLOUD_API_KEY, IBM_MONITORING_INSTANCE_ID)
    data = filter_metric_dimensions(
        "sys.cpu.user",
        "resource.label.hostname = \"web01\" AND metric.label.cpu_type = \"core\"",
        "2025-08-01T12:00:00Z",
        "2025-08-01T14:00:00Z",
    )
    print(data)
