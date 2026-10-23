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

    def compare_metric_series(
        self,
        resource_group,
        resource_name,
        metric_name,
        start_time,
        end_time,
        resource2_group,
        resource2_name,
        interval="PT1M",
    ):
        """Compares metric values for two resources or dimension filters over the same window.

        Returns a tuple (data_resource1, data_resource2) with datapoint lists.
        """
        # Resource 1 query
        query1 = {
            "aggregation": "average",
            "interval": interval,
            "metric": metric_name,
            "timespan": f"{start_time}/{end_time}",
        }
        result1 = self.client.query_resource(
            resource_id=f"/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Insights/components/{resource_name}",
            query=query1,
        )
        data1 = result1.value[0].timeseries[0].data

        # Resource 2 query
        query2 = {
            "aggregation": "average",
            "interval": interval,
            "metric": metric_name,
            "timespan": f"{start_time}/{end_time}",
        }
        result2 = self.client.query_resource(
            resource_id=f"/subscriptions/{self.subscription_id}/resourceGroups/{resource2_group}/providers/Microsoft.Insights/components/{resource2_name}",
            query=query2,
        )
        data2 = result2.value[0].timeseries[0].data

        return data1, data2
