import os
from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential


class ObservabilityClient:
    """Local helper client for Azure Monitor Metrics.
    Provides configuration and a wrapped MetricsQueryClient.
    """

    def __init__(self):
        # Credentials are read from environment variables used by DefaultAzureCredential
        self.credential = DefaultAzureCredential()
        # Azure subscription ID – required for the query client
        self.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        if not self.subscription_id:
            raise RuntimeError("AZURE_SUBSCRIPTION_ID environment variable not set")
        # Initialise the SDK client
        self.client = MetricsQueryClient(
            credential=self.credential, subscription_id=self.subscription_id
        )

    def query_metric_window(
        self,
        resource_group,
        resource_name,
        metric_name,
        start_time,
        end_time,
        interval="PT1M",
    ):
        """Query recent datapoints for a named metric over a time window.

        Returns a list of datapoint dictionaries.
        """
        query = {
            "aggregation": "total",
            "interval": interval,
            "metric": metric_name,
            "timespan": f"{start_time}/{end_time}",
        }
        result = self.client.query_resource(
            resource_id=f"/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Insights/components/{resource_name}",
            query=query,
        )
        return result.value
