import os
from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.events_api import EventsApi
from datadog_api_client.v1.model.event_create_request import EventCreateRequest

def send_rotation_summary_event(secret_name: str, status: str, rotation_date: str, notes: str = "") -> None:
    configuration = Configuration()
    # Datadog API key and Application key should be set as environment variables
    configuration.api_key['apiKeyAuth'] = os.environ.get("DD_API_KEY")
    configuration.api_key['appKeyAuth'] = os.environ.get("DD_APP_KEY")
    configuration.host = os.environ.get("DD_HOST", "https://api.datadoghq.com")

    with ApiClient(configuration) as api_client:
        api_instance = EventsApi(api_client)
        title = f"Secret Rotation Summary: {secret_name} - {status}"
        text = f"Secret '{secret_name}' rotation status: {status}. Rotation date: {rotation_date}.\nNotes: {notes}"

        body = EventCreateRequest(
            title=title,
            text=text,
            tags=[
                f"secret:{secret_name}",
                f"status:{status}",
                "source:secret-rotation-summary"
            ],
            priority="normal",
            alert_type="info" if status == "completed" else "warning"
        )

        try:
            response = api_instance.create_event(body=body)
            print(f"Datadog event sent for secret '{secret_name}'. Event ID: {response.get('event', {}).get('id')}")
        except Exception as e:
            print(f"Error sending Datadog event for secret '{secret_name}': {e}")

if __name__ == '__main__':
    # Example usage (requires DD_API_KEY, DD_APP_KEY environment variables)
    # and optional DD_HOST if not using datadoghq.com
    secret_name_example = "my-app-db-secret"
    rotation_status_example = "completed"
    rotation_date_example = "2026-09-19"
    rotation_notes_example = "Successfully rotated database credentials."

    send_rotation_summary_event(
        secret_name_example,
        rotation_status_example,
        rotation_date_example,
        rotation_notes_example
    )

    secret_name_failed = "another-api-key"
    rotation_status_failed = "failed"
    rotation_date_failed = "2026-09-19"
    rotation_notes_failed = "Failed during validation step."
    send_rotation_summary_event(
        secret_name_failed,
        rotation_status_failed,
        rotation_date_failed,
        rotation_notes_failed
    )
