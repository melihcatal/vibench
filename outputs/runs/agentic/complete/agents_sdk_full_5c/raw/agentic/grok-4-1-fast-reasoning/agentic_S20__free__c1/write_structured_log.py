from typing import Dict, Any
from observability_client import get_datadog_configuration
from observability_models import normalize_structured_log
from datadog_api_client import ApiClient
from datadog_api_client.v2.api.logs_api import LogsApi

def write_structured_log(message: str, level: str = "INFO", **kwargs: Any) -> None:
    """
    Writes a structured JSON log event to Datadog.
    """
    log_event = normalize_structured_log(message, level, **kwargs)
    configuration = get_datadog_configuration()
    with ApiClient(configuration) as api_client:
        api_instance = LogsApi(api_client)
        api_instance.submit_log(json_body=log_event)
