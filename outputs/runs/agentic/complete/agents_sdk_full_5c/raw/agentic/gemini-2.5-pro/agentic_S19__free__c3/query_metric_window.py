from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import time
from observability_client import get_monitoring_client, get_gcp_project_id

def query_cpu_utilization(project_id: str, minutes: int = 20):
    """Queries CPU utilization for a GCP project over a time window."""
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

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    
    print("Querying metric window for compute.googleapis.com/instance/cpu/utilization...")
    for result in results:
        print(f"  - Resource: {result.resource.labels['instance_id']}")
        for point in result.points:
            print(f"    {point.interval.end_time}: {point.value.double_value}")
    return results

if __name__ == "__main__":
    gcp_project = get_gcp_project_id()
    query_cpu_utilization(gcp_project)
