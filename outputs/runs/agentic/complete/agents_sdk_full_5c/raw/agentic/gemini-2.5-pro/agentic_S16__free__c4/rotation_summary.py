import os
from datetime import datetime
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import events_api
from datadog_api_client.v1.models import EventCreateRequest

from security_models import SecretRotationEvent

def post_rotation_summary(event_data: SecretRotationEvent):
    """
    Posts a summary of a secret rotation event to Datadog.

    Args:
        event_data: A Pydantic model containing details of the rotation event.
    """
    if not os.environ.get("DATADOG_API_KEY") or not os.environ.get("DATADOG_APP_KEY"):
        print("DATADOG_API_KEY and DATADOG_APP_KEY must be set.")
        return

    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = events_api.EventsApi(api_client)
        body = EventCreateRequest(
            title=f"Secret Rotation {event_data.status}: {event_data.secret_name}",
            text=event_data.details,
            tags=[
                f"source:{event_data.source_system}",
                f"secret:{event_data.secret_name}",
                f"status:{event_data.status.lower()}",
            ],
            source_type_name="my_apps",
        )

        try:
            api_response = api_instance.create_event(body)
            print("Successfully posted event to Datadog.")
            print(api_response)
        except ApiException as e:
            print(f"Exception when calling EventsApi->create_event: {e}\n")

