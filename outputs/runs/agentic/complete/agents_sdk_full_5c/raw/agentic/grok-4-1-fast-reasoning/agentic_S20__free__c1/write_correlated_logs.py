from typing import List
from observability_client import get_datadog_configuration
from observability_models import normalize_structured_log
from datadog_api_client import ApiClient
from datadog_api_client.v2.api.logs_api import LogsApi

def write_correlated_logs(correlation_id: str, messages: List[str], level: str = "INFO") -> None:
    """
    Writes correlated application log events to Datadog with shared correlation ID.
    """
    configuration = get_datadog_configuration()
    with ApiClient(configuration) as api_client:
        api_instance = LogsApi(api_client)
        for message in messages:
            log_event = normalize_structured_log(message, level, correlation_id=correlation_id)
            api_instance.submit_log(json_body=log_event)
