from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.events_api import EventsApi
from datadog_api_client.v2.model.event_attributes import EventAttributes
from datadog_api_client.v2.model.event_create_request import EventCreateRequest
from datadog_api_client.v2.model.event_type import EventType
from datetime import datetime


def summarize_rotation_status(secret_id: str, status: str, notes: str):
    """
    Summarizes secret rotation status by sending an event to Datadog.
    """
    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = EventsApi(api_client)
        body = EventCreateRequest(
            data=dict(
                attributes=EventAttributes(
                    title="Secret Rotation Summary",
                    text=f"Secret: {secret_id}\nStatus: {status}\nNotes: {notes}",
                    tags=["security", "secrets", "rotation"],
                    start_date=int(datetime.now().timestamp()),
                ),
                type=EventType("secret_rotation"),
            ),
        )
        try:
            api_response = api_instance.create_event(body=body)
            print("Successfully sent rotation summary to Datadog.")
            return api_response
        except Exception as e:
            print(f"Error sending summary to Datadog: {e}")
            return None
