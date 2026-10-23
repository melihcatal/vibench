from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import time
from observability_client import get_monitoring_client, get_gcp_project_id

def _get_series(client, project_name, filter_str, interval):
    """Helper to fetch a single time series."""
    return client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

def compare_cpu_between_instances(project_id: str, instance_id_a: str, instance_id_b: str, minutes: int = 15):
    """Compares CPU utilization between two specific instances."""
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": Timestamp(seconds=seconds, nanos=nanos),
            "start_time": Timestamp(seconds=(seconds - 60 * minutes), nanos=nanos),
        }
    )

    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    filter_a = f'metric.type = "{metric_type}" AND resource.labels.instance_id = "{instance_id_a}"'
    filter_b = f'metric.type = "{metric_type}" AND resource.labels.instance_id = "{instance_id_b}"'

    series_a = list(_get_series(client, project_name, filter_a, interval))
    series_b = list(_get_series(client, project_name, filter_b, interval))

    print(f"Comparing CPU utilization between '{instance_id_a}' and '{instance_id_b}'...")

    if series_a:
        print(f"\nResults for {instance_id_a}:")
        for point in series_a[0].points:
            print(f"  {point.interval.end_time}: {point.value.double_value:.4f}")
    else:
        print(f"\nNo data found for {instance_id_a}.")

    if series_b:
        print(f"\nResults for {instance_id_b}:")
        for point in series_b[0].points:
            print(f"  {point.interval.end_time}: {point.value.double_value:.4f}")
    else:
        print(f"\nNo data found for {instance_id_b}.")
        
    return series_a, series_b

if __name__ == "__main__":
    gcp_project = get_gcp_project_id()
    # Replace with real instance IDs from your project to see data
    instance_1 = "instance-a-to-replace"
    instance_2 = "instance-b-to-replace"
    compare_cpu_between_instances(gcp_project, instance_1, instance_2)
