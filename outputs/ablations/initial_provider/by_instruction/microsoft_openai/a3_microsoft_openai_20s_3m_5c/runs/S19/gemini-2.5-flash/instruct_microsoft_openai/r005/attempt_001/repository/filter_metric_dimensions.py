import os
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient
from observability_models import MetricDimensionRequest, MetricDimensionResponse

def filter_metric_dimensions(request: MetricDimensionRequest) -> MetricDimensionResponse:
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)

    resource_id = os.environ.get("AZURE_MONITOR_RESOURCE_ID")
    if not resource_id:
        raise ValueError("AZURE_MONITOR_RESOURCE_ID environment variable not set.")

    start_time_dt = datetime.fromisoformat(request.start_time)
    end_time_dt = datetime.fromisoformat(request.end_time)

    # Construct OData filter from dimensions
    filter_parts = []
    for dim, val in request.dimensions.items():
        filter_parts.append(f"{dim} eq '{val}'")
    odata_filter = " and ".join(filter_parts)

    try:
        response = client.query_resource(
            resource_id=resource_id,
            metric_names=[request.metric_name],
            timespan=(start_time_dt, end_time_dt),
            filter=odata_filter,
            # Assuming default interval and aggregation for simplicity, or can be added to request model
            granularity=timedelta(minutes=5), # Defaulting to 5 min granularity for dimension filtering
            aggregations=["AVERAGE"],
        )
    except Exception as e:
        raise RuntimeError(f"Failed to query Azure Monitor metrics with dimensions: {e}")

    timeseries_data = []
    for metric in response.metrics:
        for ts in metric.timeseries:
            for dp in ts.data:
                timeseries_data.append({
                    "timestamp": dp.timestamp.isoformat(),
                    "value": dp.average,
                    "dimensions": {dim.name: dim.value for dim in ts.metadata}
                })
    
    return MetricDimensionResponse(timeseries=timeseries_data)

if __name__ == "__main__":
    # Example Usage
    request = MetricDimensionRequest(
        metric_name="NetworkInTotal",
        start_time=(datetime.utcnow() - timedelta(hours=1)).isoformat(),
        end_time=datetime.utcnow().isoformat(),
        dimensions={
            "InterfaceName": "Wireless",
            "Computer": "myvm"
        }
    )
    try:
        response = filter_metric_dimensions(request)
        print("Query with dimensions successful!")
        for dp in response.timeseries:
            print(f"Timestamp: {dp['timestamp']}, Value: {dp['value']}, Dimensions: {dp['dimensions']}")
    except Exception as e:
        print(f"Error: {e}")
