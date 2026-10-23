from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import time
from observability_client import get_monitoring_client, get_gcp_project_id

def get_aggregated_network_traffic(project_id: str, minutes: int = 60):
    """Retrieves aggregated network traffic stats."""
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

    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 600},  # 10 minutes
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_SUM,
            "group_by_fields": ["resource.zone"],
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "compute.googleapis.com/instance/network/received_bytes_count"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    
    print("Aggregating metric stats for compute.googleapis.com/instance/network/received_bytes_count...")
    for result in results:
        print(f"  - Zone: {result.resource.labels['zone']}")
        for point in result.points:
            print(f"    {point.interval.end_time}: {point.value.double_value}")
    return results

if __name__ == "__main__":
    gcp_project = get_gcp_project_id()
    get_aggregated_network_traffic(gcp_project)
