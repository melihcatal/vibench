import os
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import MetricAggregationResponse

def get_aggregated_metric_statistics(
    resource_id: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    aggregation: str # e.g., "Average", "Total", "Maximum", "Minimum", "Count"
) -> MetricAggregationResponse:
    """
    Retrieves aggregated statistics for a metric over a time window using Azure Monitor.
    The resource_id should be a fully qualified Azure resource ID.
    """
    azure_subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    if not azure_subscription_id:
        raise ValueError("AZURE_SUBSCRIPTION_ID environment variable not set.")

    # Note: For Azure Monitor, DefaultAzureCredential will pick up credentials from env vars (AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID) or other configured methods.
    # OpenAI API Key is not directly used for this file but passed for client initialization consistency.
    dummy_openai_api_key = os.environ.get("OPENAI_API_KEY", "dummy_key") 

    client = ObservabilityClient(
        openai_api_key=dummy_openai_api_key,
        azure_subscription_id=azure_subscription_id
    )
    
    aggregation_response = client.get_azure_monitor_aggregated_metric_stats(
        resource_id=resource_id,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        aggregation=aggregation
    )
    return aggregation_response
