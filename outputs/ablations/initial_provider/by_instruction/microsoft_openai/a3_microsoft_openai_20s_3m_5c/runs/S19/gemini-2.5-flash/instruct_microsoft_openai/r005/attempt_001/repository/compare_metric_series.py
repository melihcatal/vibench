import os
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient
from observability_models import MetricComparisonRequest, MetricComparisonResponse

def compare_metric_series(request: MetricComparisonRequest) -> MetricComparisonResponse:
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)

    resource_id = os.environ.get("AZURE_MONITOR_RESOURCE_ID")
    if not resource_id:
        raise ValueError("AZURE_MONITOR_RESOURCE_ID environment variable not set.")

    start_time_dt = datetime.fromisoformat(request.start_time)
    end_time_dt = datetime.fromisoformat(request.end_time)

    series1_data = []
    series2_data = []

    try:
        # Query for series 1
        response1 = client.query_resource(
            resource_id=resource_id,
            metric_names=[request.metric_name],
            timespan=(start_time_dt, end_time_dt),
            filter=request.filter1,
            granularity=timedelta(minutes=5),
            aggregations=["AVERAGE"],
        )
        for metric in response1.metrics:
            for ts in metric.timeseries:
                for dp in ts.data:
                    series1_data.append({
                        "timestamp": dp.timestamp.isoformat(),
                        "value": dp.average,
                    })

        # Query for series 2
        response2 = client.query_resource(
            resource_id=resource_id,
            metric_names=[request.metric_name],
            timespan=(start_time_dt, end_time_dt),
            filter=request.filter2,
            granularity=timedelta(minutes=5),
            aggregations=["AVERAGE"],
        )
        for metric in response2.metrics:
            for ts in metric.timeseries:
                for dp in ts.data:
                    series2_data.append({
                        "timestamp": dp.timestamp.isoformat(),
                        "value": dp.average,
                    })

    except Exception as e:
        raise RuntimeError(f"Failed to compare Azure Monitor metric series: {e}")
    
    # For comparison, we will return both series. The actual comparison logic
    # could be implemented here or in a consuming function.
    return MetricComparisonResponse(
        comparison_result={
            "series1": series1_data,
            "series2": series2_data,
            "metric_name": request.metric_name,
        }
    )

if __name__ == "__main__":
    # Example Usage
    request = MetricComparisonRequest(
        metric_name="CpuUtilization",
        start_time=(datetime.utcnow() - timedelta(hours=1)).isoformat(),
        end_time=datetime.utcnow().isoformat(),
        filter1="Computer eq 'myvm1'",
        filter2="Computer eq 'myvm2'"
    )
    try:
        response = compare_metric_series(request)
        print("Metric series comparison successful!")
        print("Series 1 data:", response.comparison_result["series1"])
        print("Series 2 data:", response.comparison_result["series2"])
    except Exception as e:
        print(f"Error: {e}")
