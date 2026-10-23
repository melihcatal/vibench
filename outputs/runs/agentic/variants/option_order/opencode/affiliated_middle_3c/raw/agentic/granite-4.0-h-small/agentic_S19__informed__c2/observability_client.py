import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()


class BaseClient(ABC):
    @abstractmethod
    def query_metric_window(self, *args, **kwargs):
        pass

    @abstractmethod
    def aggregate_metric_stats(self, *args, **kwargs):
        pass

    @abstractmethod
    def filter_metric_dimensions(self, *args, **kwargs):
        pass

    @abstractmethod
    def compare_metric_series(self, *args, **kwargs):
        pass


class AzureMonitorClient:
    def __init__(self):
        self.credential = os.getenv(
            "AZURE_CREDENTIAL"
        )  # placeholder for actual Azure credential handling

    def query_metric_window(self, resource_id, metric_name, start_time, end_time):
        # Azure Monitor SDK query implementation (omitted details)
        return {"query": "Azure Monitor"}

    def aggregate_metric_stats(self, resource_id, metric_name, start_time, end_time):
        return {"aggregate": "Azure Monitor"}

    def filter_metric_dimensions(
        self, resource_id, metric_name, filter_expr, start_time, end_time
    ):
        return {"filter": "Azure Monitor"}

    def compare_metric_series(
        self,
        resource_id1,
        metric_name,
        filter_expr1,
        resource_id2,
        filter_expr2,
        start_time,
        end_time,
    ):
        return {"compare": "Azure Monitor"}


# Additional providers can be added similarly, e.g., Boto3CloudWatchClient, IBMWatsonxClient, etc.

# Helper to instantiate client based on environment variable or config
CLIENT_FACTORY = {
    "AZURE_MONITOR": AzureMonitorClient,
    # 'CLOUDWATCH': Boto3CloudWatchClient,
    # 'WATSONX': IBMWatsonxClient,
    # 'CLOUDMONITOR': AlibabaCloudMonitorClient,
}


def get_client(provider_name):
    if provider_name not in CLIENT_FACTORY:
        raise ValueError(f"Unsupported provider: {provider_name}")
    return CLIENT_FACTORY[provider_name]()
