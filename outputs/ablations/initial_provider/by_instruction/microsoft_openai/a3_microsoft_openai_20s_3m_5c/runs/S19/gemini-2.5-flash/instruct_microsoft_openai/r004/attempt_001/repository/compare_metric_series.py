import os
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import MetricComparisonResponse

def compare_metric_values_for_resources(
    project_id: str,
    metric_type: str,
    filter_a: str, # Google Cloud Monitoring filter string for resource/dimension set A
    filter_b: str, # Google Cloud Monitoring filter string for resource/dimension set B
    start_time: datetime,
    end_time: datetime
) -> MetricComparisonResponse:
    """
    Compares metric values for two resources or dimension filters over the same window
    using Google Cloud Monitoring.
    """
    google_project_id = os.environ.get("GOOGLE_PROJECT_ID")
    if not google_project_id:
        raise ValueError("GOOGLE_PROJECT_ID environment variable not set.")

    # OpenAI API Key is not directly used for this file but passed for client initialization consistency.
    dummy_openai_api_key = os.environ.get("OPENAI_API_KEY", "dummy_key") 

    client = ObservabilityClient(
        openai_api_key=dummy_openai_api_key,
        google_project_id=google_project_id
    )

    comparison_response = client.get_google_cloud_monitoring_metric_series(
        project_id=project_id,
        metric_type=metric_type,
        filter_a=filter_a,
        filter_b=filter_b,
        start_time=start_time,
        end_time=end_time
    )
    return comparison_response
