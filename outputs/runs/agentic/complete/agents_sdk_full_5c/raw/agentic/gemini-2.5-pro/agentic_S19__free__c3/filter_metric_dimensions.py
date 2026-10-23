from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import time
from observability_client import get_monitoring_client, get_gcp_project_id

def query_disk_for_instance(project_id: str, instance_id: str, minutes: int = 30):
    """Queries disk read bytes for a specific instance."""
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

    # Filter by both metric type and a specific resource label (dimension)
    filter_str = (
        'metric.type = "compute.googleapis.com/instance/disk/read_bytes_count" AND '
        f'resource.labels.instance_id = "{instance_id}"'
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.HEADERS,
        }
    )
    
    print(f"Querying with dimension filter for instance_id='{instance_id}'...")
    for result in results:
        print(f"  - Metric: {result.metric.type}")
        print(f"  - Resource Labels: {result.resource.labels}")
    
    if not list(results):
         print(f"No data found for instance '{instance_id}'. It may be invalid or have no recent data.")

    return results

if __name__ == "__main__":
    gcp_project = get_gcp_project_id()
    # Replace with a real instance ID from your project to see data
    example_instance_id = "default-instance-id-to-replace" 
    query_disk_for_instance(gcp_project, example_instance_id)
