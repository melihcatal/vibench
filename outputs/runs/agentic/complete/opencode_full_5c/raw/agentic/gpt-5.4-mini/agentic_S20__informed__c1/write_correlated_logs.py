from observability_client import client_from_env
from observability_models import LogEvent


def write_correlated_logs(correlation_id: str, messages):
    client = client_from_env()
    written = []
    for index, message in enumerate(messages):
        event = LogEvent(
            message=message,
            severity="INFO",
            correlation_id=correlation_id,
            fields={"step": index},
        )
        written.append(client.put_event(event))
    return written
