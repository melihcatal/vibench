import os
from datadog_api_client.v2 import ApiClient, ApiException
from datadog_api_client.v2.api import events_api
from datadog_api_client.v2.models import EventAttributes, EventCreateRequest, EventType


def rotation_summary(secret_name: str, status: str):
    """
    Summarize secret rotation status by sending an event to Datadog.
    """
    configuration = ApiClient.configuration()
    configuration.api_key["apiKeyAuth"] = os.environ.get("DATADOG_API_KEY")
    configuration.api_key["appKeyAuth"] = os.environ.get("DATADOG_APP_KEY")

    with ApiClient(configuration) as api_client:
        api_instance = events_api.EventsApi(api_client)
        body = EventCreateRequest(
            data=dict(
                attributes=EventAttributes(
                    title="Secret Rotation Summary",
                    text=f"Secret '{secret_name}' rotation status: {status}",
                ),
                type=EventType.INFO,
            ),
        )

        try:
            api_response = api_instance.create_event(body)
            return api_response
        except ApiException as e:
            print(f"Exception when calling EventsApi->create_event: {e}\n")
            return None
