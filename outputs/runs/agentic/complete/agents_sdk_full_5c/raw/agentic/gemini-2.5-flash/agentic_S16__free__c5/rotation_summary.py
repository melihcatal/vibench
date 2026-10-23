import os
import datetime
from datadog_api_client.v2 import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_series import MetricSeries
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType

def post_secret_rotation_metric(metric_name: str, value: float, secret_name: str, status: str) -> None:
    """
    Posts a custom metric to Datadog summarizing secret rotation status.

    Args:
        metric_name: The name of the metric (e.g., "secret.rotation.status").
        value: The numeric value of the metric (e.g., 0 for failed, 1 for success).
        secret_name: The name of the secret being rotated.
        status: The rotation status (e.g., "success", "failure", "pending").
    """
    configuration = Configuration()
    # Datadog API key and Application key are usually set as environment variables (DD_API_KEY, DD_APP_KEY)
    # but can also be explicitly passed to Configuration()
    # configuration.api_key["apiKeyAuth"] = os.getenv("DD_API_KEY")
    # configuration.api_key["appKeyAuth"] = os.getenv("DD_APP_KEY")

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        body = MetricPayload(
            series=[
                MetricSeries(
                    metric=metric_name,
                    type=MetricIntakeType.GAUGE,
                    points=[
                        MetricPoint(
                            timestamp=int(datetime.datetime.now().timestamp()),
                            value=value,
                        ),
                    ],
                    tags=[
                        f"secret_name:{secret_name}",
                        f"rotation_status:{status}"
                    ],
                    resources=[
                        # Optional: Add host or other resource tags if relevant
                        # datadog_api_client.v2.model.metric_resource.MetricResource(
                        #     name="my-host",
                        #     type="host",
                        # ),
                    ]
                ),
            ],
        )

        try:
            response = api_instance.submit_metrics(body=body)
            # print(f"Datadog metric submission response: {response}")
        except Exception as e:
            raise RuntimeError(f"Error submitting metric to Datadog: {e}")

if __name__ == '__main__':
    # This is an example of how you might use it.
    # DD_API_KEY and DD_APP_KEY must be set as environment variables.
    #
    # try:
    #     print("Posting secret rotation success metric...")
    #     post_secret_rotation_metric("secret.rotation.status", 1.0, "api-key-prod", "success")
    #     print("Metric posted successfully (check your Datadog account).")
    #
    #     print("Posting secret rotation failure metric...")
    #     post_secret_rotation_metric("secret.rotation.status", 0.0, "db-credential-dev", "failure")
    #     print("Metric posted successfully (check your Datadog account).")
    # except RuntimeError as e:
    #     print(f"Failed to post metric: {e}")
    pass
