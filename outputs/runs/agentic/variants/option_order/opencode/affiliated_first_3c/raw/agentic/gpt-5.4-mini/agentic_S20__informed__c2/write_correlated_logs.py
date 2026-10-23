from observability_client import DatadogLogsClient
from observability_models import build_log_record


def write_correlated_logs(request_id: str, messages):
    client = DatadogLogsClient()
    results = []
    for index, message in enumerate(messages):
        record = build_log_record(
            message,
            "info",
            event_type="correlated",
            request_id=request_id,
            sequence=index,
        )
        results.append(client.write_log(record))
    return results
