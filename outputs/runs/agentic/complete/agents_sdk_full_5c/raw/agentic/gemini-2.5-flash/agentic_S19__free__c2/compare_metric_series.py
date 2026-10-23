import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

# Google Cloud project ID
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

def compare_metric_series(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    duration_minutes: int = 60,
    filter_series_a: str = None,
    filter_series_b: str = None,
):
    """Compares metric values for two resources or dimension filters over the same window."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    def fetch_series(series_filter):
        full_filter = f'metric.type = "{metric_type}"'
        if series_filter:
            full_filter += f' AND {series_filter}'

        response = client.list_time_series(
            request={
                "name": project_name,
                "filter": full_filter,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            }
        )
        series_data = []
        for ts in response.time_series:
            for point in ts.points:
                series_data.append(
                    {
                        "metric": ts.metric.type,
                        "resource_labels": dict(ts.resource.labels),
                        "value": point.value.double_value or point.value.int64_value,
                        "timestamp": point.interval.end_time.timestamp(),
                    }
                )
        return series_data

    series_a_data = fetch_series(filter_series_a)
    series_b_data = fetch_series(filter_series_b)

    return {"series_a": series_a_data, "series_b": series_b_data}

if __name__ == "__main__":
    # Example usage: Replace with your actual project ID and metric type
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # comparison_results = compare_metric_series(
    #     PROJECT_ID,
    #     "compute.googleapis.com/instance/cpu/utilization",
    #     datetime.utcnow(),
    #     duration_minutes=10,
    #     filter_series_a='resource.instance_name = "instance-1" ',
    #     filter_series_b='resource.instance_name = "instance-2" '
    # )
    # print("Series A Data:", comparison_results["series_a"])
    # print("Series B Data:", comparison_results["series_b"])
    pass
