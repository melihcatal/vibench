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
        self.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        if not self.subscription_id:
            raise RuntimeError("AZURE_SUBSCRIPTION_ID environment variable not set")
        self.client = MetricsQueryClient(
            credential=self.credential, subscription_id=self.subscription_id
        )

    def aggregate_metric_stats(
        self,
        resource_group,
        resource_name,
        metric_name,
        start_time,
        end_time,
        aggregation="average",
    ):
        """Retrieve aggregated statistics for a metric over a time window.

        Args:
            aggregation: one of 'average', 'total', 'maximum', 'minimum', 'count'
        """
        query = {
            "aggregation": aggregation,
            "metric": metric_name,
            "timespan": f"{start_time}/{end_time}",
        }
        result = self.client.query_resource(
            resource_id=f"/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Insights/components/{resource_name}",
            query=query,
        )
        return result.value[0].timeseries[0].data
