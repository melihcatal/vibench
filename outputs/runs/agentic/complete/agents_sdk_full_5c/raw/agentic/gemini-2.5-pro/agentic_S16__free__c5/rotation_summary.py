
import os
from datetime import datetime
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.events_api import EventsApi
from datadog_api_client.v1.model.event_create_request import EventCreateRequest

def post_rotation_summary_event(secret_name: str, status: str):
    """
    Posts an event to Datadog summarizing a secret rotation.

    Args:
        secret_name: The name of the secret that was rotated.
        status: The status of the rotation (e.g., 'SUCCESS', 'FAILURE').
    """
    # Ensure API key and site are configured
    if "DD_API_KEY" not in os.environ or "DD_SITE" not in os.environ:
        print("DD_API_KEY and DD_SITE environment variables must be set.")
        return

    configuration = Configuration()
    api_client = ApiClient(configuration)
    events_api = EventsApi(api_client)

    event_title = f"Secret Rotation {status.capitalize()}: {secret_name}"
    event_text = f"%%%\nSecret **{secret_name}** rotation status: **{status}**.\n\nCheck logs for more details.\n@ops-team\n%%%"
    
    body = EventCreateRequest(
        title=event_title,
        text=event_text,
        tags=[f"secret-rotation", f"secret:{secret_name}", f"status:{status.lower()}"],
        alert_type="success" if status == 'SUCCESS' else "error",
    )

    try:
        response = events_api.create_event(body=body)
        print(f"Successfully posted Datadog event for '{secret_name}'. Status: {response.status}")
    except Exception as e:
        print(f"Error posting event to Datadog: {e}")

if __name__ == '__main__':
    # Example usage
    # Set DD_API_KEY and DD_SITE environment variables
    SECRET_ID = "production/database/credentials"
    post_rotation_summary_event(SECRET_ID, 'SUCCESS')
    post_rotation_summary_event("billing-api-key", 'FAILURE')
