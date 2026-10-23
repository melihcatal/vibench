from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metric_series import MetricSeries
from datadog_api_client.v1.model.series import Series
import os
from datetime import datetime
from typing import List, Dict, Any

def summarize_rotation_status(secret_id: str, provider: str, status: str, last_rotation_date: datetime = None, tags: List[str] = None):
    """
    Summarizes secret rotation status by sending a metric to Datadog.
    """
    configuration = Configuration()
    # Datadog API key and Application key should be set as environment variables
    # DD_API_KEY and DD_APPLICATION_KEY
    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)

        metric_value = 1.0 if status == "Successful" else 0.0
        
        series_tags = [f"secret_id:{secret_id}", f"provider:{provider}", f"status:{status}"]
        if tags:
            series_tags.extend(tags)

        body = MetricSeries(
            series=[
                Series(
                    metric="secret.rotation.status",
                    points=[[datetime.now().timestamp(), metric_value]],
                    type="gauge",
                    tags=series_tags,
                ),
            ],
        )

        try:
            response = api_instance.submit_metrics(body=body)
            print(f"Datadog metrics submission response: {response}")
        except Exception as e:
            raise RuntimeError(f"Failed to submit rotation summary to Datadog: {e}")

if __name__ == '__main__':
    # Example usage (requires DD_API_KEY and DD_APPLICATION_KEY environment variables)
    # Set DD_API_KEY and DD_APPLICATION_KEY before running
    # summarize_rotation_status("my-api-key", "azure_key_vault", "Successful", datetime.now())
    pass
