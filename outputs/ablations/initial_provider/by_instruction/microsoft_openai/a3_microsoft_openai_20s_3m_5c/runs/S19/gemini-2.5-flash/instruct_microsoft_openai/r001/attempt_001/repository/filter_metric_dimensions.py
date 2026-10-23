import os
from datetime import datetime, timedelta
from typing import Dict, Optional

from observability_client import GoogleCloudMetricsClient
from observability_models import MetricQueryRequest, MetricQueryResponse

def filter_metric_dimensions(
    project_id: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimensions_filter: Dict[str, str],
    interval: Optional[str] = None
) -> MetricQueryResponse:
    """
    Queries metric data filtered by resource labels or dimensions using Google Cloud Monitoring.

    Args:
        project_id: The Google Cloud Project ID.
        metric_name: The full metric type (e.g., "compute.googleapis.com/instance/cpu/usage_time").
        start_time: The start of the time window.
        end_time: The end of the time window.
        dimensions_filter: A dictionary of dimension names and values to filter the metrics.
                           These will be treated as metric labels for filtering.
        interval: The aggregation interval (e.g., 'PT5M' for 5 minutes). Optional.

    Returns:
        A MetricQueryResponse object containing the queried metric data.
    """
    client = GoogleCloudMetricsClient()
    
    request = MetricQueryRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimensions_filter=dimensions_filter,
        interval=interval
    )
    
    response = client.filter_metric_dimensions(request, project_id)
    return response

if __name__ == '__main__':
    # Example usage (requires GOOGLE_CLOUD_PROJECT_ID environment variable to be set)
    # And appropriate Google Cloud credentials configured (e.g., gcloud auth application-default login)

    project_id_example = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    
    end_time_example = datetime.utcnow()
    start_time_example = end_time_example - timedelta(hours=1)
    
    # Example metric for Google Compute Engine CPU usage
    # Make sure this metric type and labels exist in your project.
    example_metric_name = "compute.googleapis.com/instance/cpu/utilization"
    example_dimensions_filter = {"instance_name": "my-instance-1"}

    if project_id_example:
        print(f"Querying metric '{example_metric_name}' for project '{project_id_example}' with dimensions {example_dimensions_filter}")
        try:
            metric_data = filter_metric_dimensions(
                project_id=project_id_example,
                metric_name=example_metric_name,
                start_time=start_time_example,
                end_time=end_time_example,
                dimensions_filter=example_dimensions_filter,
                interval="PT1M"
            )

            print(f"\nMetric Name: {metric_data.metric_name}")
            print("Data Points:")
            for dp in metric_data.data_points:
                print(f"  Timestamp: {dp.timestamp}, Value: {dp.value}, Dimensions: {dp.dimensions}")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable for example usage.")
