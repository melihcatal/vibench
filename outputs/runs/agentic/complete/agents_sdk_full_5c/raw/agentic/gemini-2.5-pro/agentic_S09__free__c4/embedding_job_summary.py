import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor

def get_job_summary(monitor_id: int) -> dict:
    """
    Retrieves a summary for a job represented by a Datadog monitor.

    Args:
        monitor_id: The ID of the Datadog monitor.

    Returns:
        A dictionary containing summary information about the monitor.
    """
    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = os.getenv("DD_API_KEY")
    configuration.api_key["appKeyAuth"] = os.getenv("DD_APP_KEY")

    with ApiClient(configuration) as api_client:
        api_instance = MonitorsApi(api_client)
        monitor: Monitor = api_instance.get_monitor(monitor_id)

        return {
            "id": monitor.id,
            "name": monitor.name,
            "status": monitor.overall_state.value,
            "type": monitor.type.value,
            "query": monitor.query,
            "last_modified": monitor.modified.isoformat(),
        }
