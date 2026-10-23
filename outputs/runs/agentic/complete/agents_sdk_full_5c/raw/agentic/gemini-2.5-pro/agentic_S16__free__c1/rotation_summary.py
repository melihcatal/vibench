import os
from datetime import datetime

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.events_api import EventsApi
from datadog_api_client.v1.model.event_create_request import EventCreateRequest


def report_rotation_status_to_datadog(secret_name: str, status: str, success: bool):
    """
    Posts an event to DataDog summarizing a secret rotation event.

    Args:
        secret_name: The name of the secret that was rotated.
        status: A descriptive status message.
        success: A boolean indicating if the rotation was successful.
    """
    if "DD_API_KEY" not in os.environ or "DD_APP_KEY" not in os.environ:
        raise ValueError("DATADOG_API_KEY and DATADOG_APP_KEY env vars must be set.")
    
    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = EventsApi(api_client)
        
        event_body = EventCreateRequest(
            title=f"Secret Rotation for {secret_name}",
            text=f"Rotation process for secret '{secret_name}' finished with status: {status}",
            tags=[f"security:secret_rotation", f"secret:{secret_name}"],
            alert_type="success" if success else "error",
            source_type_name="my_apps",
        )

        try:
            api_response = api_instance.create_event(body=event_body)
            print(f"Successfully sent event to Datadog: {api_response['status']}")
        except Exception as e:
            print(f"Exception when calling EventsApi->create_event: {e}")
            raise

