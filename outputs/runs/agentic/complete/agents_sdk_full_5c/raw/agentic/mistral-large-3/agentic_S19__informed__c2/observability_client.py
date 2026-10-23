from google.cloud import monitoring_v3
from google.api_core.client_options import ClientOptions
from typing import Union, Type, TypeVar
import os

T = TypeVar('T')


def get_observability_client(client_type: Union[str, Type[T]]) -> Union[T, str]:
    """Provide a configured client or configuration value for Google Cloud Monitoring."""
    if isinstance(client_type, str):
        if client_type == "GOOGLE_CLOUD_PROJECT":
            return os.getenv("GOOGLE_CLOUD_PROJECT", "")
        raise ValueError(f"Unsupported config key: {client_type}")

    if client_type == monitoring_v3.MetricServiceClient:
        client_options = ClientOptions(
            api_endpoint=os.getenv("GOOGLE_CLOUD_MONITORING_ENDPOINT", "monitoring.googleapis.com")
        )
        return client_type(client_options=client_options)

    raise ValueError(f"Unsupported client type: {client_type}")