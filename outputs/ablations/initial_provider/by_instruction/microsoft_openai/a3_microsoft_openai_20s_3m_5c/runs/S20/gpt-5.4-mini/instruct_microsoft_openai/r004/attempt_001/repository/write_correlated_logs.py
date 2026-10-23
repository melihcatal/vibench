from observability_client import get_client
from observability_models import normalize_log_event


def write_correlated_logs(events, correlation_id):
    client = get_client()
    normalized = []
    for event in events:
        item = normalize_log_event(event)
        item["correlation_id"] = correlation_id
        normalized.append(item)
    return client.responses.create(model="gpt-4.1-mini", input=str(normalized))
