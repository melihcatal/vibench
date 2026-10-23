import os
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient
from observability_models import MetricStatRequest, MetricStatResponse

def aggregate_metric_stats(request: MetricStatRequest) -> MetricStatResponse:
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)

    resource_id = os.environ.get("AZURE_MONITOR_RESOURCE_ID")
    if not resource_id:
        raise ValueError("AZURE_MONITOR_RESOURCE_ID environment variable not set.")

    start_time_dt = datetime.fromisoformat(request.start_time)
    end_time_dt = datetime.fromisoformat(request.end_time)

    try:
        response = client.query_resource(
            resource_id=resource_id,
            metric_names=[request.metric_name],
            timespan=(start_time_dt, end_time_dt),
            interval=timedelta(minutes=int(request.interval.replace('PT', '').replace('M', ''))),
            granularity=timedelta(minutes=int(request.interval.replace('PT', '').replace('M', ''))),
            aggregations=[request.aggregation.upper()],
            filter=request.filter if request.filter else None,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to query Azure Monitor metrics for aggregation: {e}")

    aggregated_value = 0.0
    unit = "unknown"
    count = 0

    for metric in response.metrics:
        for ts in metric.timeseries:
            for dp in ts.data:
                value = getattr(dp, request.aggregation.lower())
                if value is not None:
                    aggregated_value += value
                    count += 1
        if metric.unit:
            unit = str(metric.unit.value) # Convert to string

    if count > 0 and request.aggregation.lower() == "average":
        aggregated_value /= count
    elif count == 0: # Handle case where no data points were found.
        aggregated_value = 0.0

    return MetricStatResponse(value=aggregated_value, unit=unit)

if __name__ == "__main__":
    # Example Usage
    request = MetricStatRequest(
        metric_name="ProcessorTime",
        start_time=(datetime.utcnow() - timedelta(hours=1)).isoformat(),
        end_time=datetime.utcnow().isoformat(),
        interval="PT5M",
        aggregation="Average",
        filter="Computer eq 'myvm'"
    )
    try:
        response = aggregate_metric_stats(request)
        print(f"Aggregated {request.aggregation} for {request.metric_name}: {response.value} {response.unit}")
    except Exception as e:
        print(f"Error: {e}")
