import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from observability_client import AzureMonitorMetricsClient
from observability_models import MetricQueryRequest

def aggregate_metric_stats(
    metric_name: str,
    resource_id: str,
    start_time: datetime,
    end_time: datetime,
    aggregations: List[str],
    interval: Optional[str] = "PT1H" # Default to 1-hour interval
) -> Dict[str, Any]:
    """
    Retrieves aggregated statistics for a metric over a time window using Azure Monitor.

    Args:
        metric_name: The name of the metric to query.
        resource_id: The Azure resource ID (e.g., /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName})
        start_time: The start of the time window.
        end_time: The end of the time window.
        aggregations: A list of aggregation types (e.g., ["Average", "Maximum", "Minimum", "Total", "Count"]).
        interval: The aggregation interval (e.g., 'PT1H' for 1 hour, 'PT5M' for 5 minutes).

    Returns:
        A dictionary containing the aggregated metric statistics.
    """
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    if not subscription_id:
        raise ValueError("AZURE_SUBSCRIPTION_ID environment variable not set.")
    
    client = AzureMonitorMetricsClient(subscription_id=subscription_id)
    
    request = MetricQueryRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        interval=interval
    )
    
    response = client.aggregate_metric_stats(request, resource_id, aggregations)
    return response

if __name__ == '__main__':
    # Example usage (requires AZURE_SUBSCRIPTION_ID and AZURE_RESOURCE_ID environment variables to be set)
    # Replace with your actual resource ID, metric name, and time window
    # For instance, a VM resource ID could look like:
    # /subscriptions/{subId}/resourceGroups/{rgName}/providers/Microsoft.Compute/virtualMachines/{vmName}

    end_time_example = datetime.utcnow()
    start_time_example = end_time_example - timedelta(hours=6)
    
    # Example: Query 'bytes_received_total' for a hypothetical resource
    # Ensure you have a valid Azure resource ID and a metric that exists for it.
    example_resource_id = os.environ.get("AZURE_RESOURCE_ID")
    example_metric_name = "SuccessfulCalls"
    example_aggregations = ["Average", "Total"]

    if example_resource_id:
        print(f"Querying aggregated stats for metric '{example_metric_name}' on resource '{example_resource_id}' from {start_time_example} to {end_time_example}")
        try:
            stats = aggregate_metric_stats(
                metric_name=example_metric_name,
                resource_id=example_resource_id,
                start_time=start_time_example,
                end_time=end_time_example,
                aggregations=example_aggregations,
                interval="PT5M"
            )
            print("\nAggregated Metric Statistics:")
            print(stats)
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("Please set AZURE_RESOURCE_ID environment variable for example usage.")
