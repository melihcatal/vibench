import os
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient
from observability_models import MetricQueryRequest, MetricQueryResponse

def query_metric_window(request: MetricQueryRequest) -> MetricQueryResponse:
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)

    resource_id = os.environ.get("AZURE_MONITOR_RESOURCE_ID")
    if not resource_id:
        raise ValueError("AZURE_MONITOR_RESOURCE_ID environment variable not set.")

    # Convert string times to datetime objects
    start_time_dt = datetime.fromisoformat(request.start_time)
    end_time_dt = datetime.fromisoformat(request.end_time)

    # Azure Monitor Metrics supports ISO 8601 duration strings for interval, e.g., 'PT1H', 'PT5M'
    # The request.interval is already in this format.

    # The metrics_query method in azure-monitor-query SDK directly handles these parameters
    # Note: The filter parameter for Azure Monitor is OData compliant. 
    # The current request.filter is a generic string, assuming it's already OData compliant for Azure.
    try:
        response = client.query_resource(
            resource_id=resource_id,
            metric_names=[request.metric_name],
            timespan=(start_time_dt, end_time_dt),
            interval=timedelta(minutes=int(request.interval.replace('PT', '').replace('M', ''))), # Convert PTnM to timedelta
            granularity=timedelta(minutes=int(request.interval.replace('PT', '').replace('M', ''))),
            aggregations=[request.aggregation.upper()], # Aggregation needs to be uppercase
            filter=request.filter if request.filter else None,
            # For more complex scenarios, dimensions can be specified here.
        )
    except Exception as e:
        raise RuntimeError(f"Failed to query Azure Monitor metrics: {e}")

    timeseries_data = []
    for metric in response.metrics:
        for ts in metric.timeseries:
            for dp in ts.data:
                timeseries_data.append({
                    "timestamp": dp.timestamp.isoformat(),
                    "value": getattr(dp, request.aggregation.lower()), # e.g., dp.average
                })
    
    return MetricQueryResponse(timeseries=timeseries_data)

if __name__ == "__main__":
    # Example Usage (requires AZURE_MONITOR_RESOURCE_ID to be set)
    # and Azure authentication configured (e.g., Azure CLI logged in)
    request = MetricQueryRequest(
        metric_name="ProcessorTime",
        start_time=(datetime.utcnow() - timedelta(hours=1)).isoformat(),
        end_time=datetime.utcnow().isoformat(),
        interval="PT5M",
        aggregation="Average",
    )
    try:
        response = query_metric_window(request)
        print("Query successful!")
        for dp in response.timeseries:
            print(f"Timestamp: {dp['timestamp']}, Value: {dp['value']}")
    except Exception as e:
        print(f"Error: {e}")
