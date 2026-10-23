import requests
from observability_client import (
    get_log_service_url,
    get_auth_header,
    parse_log_response,
)

MAX_RECENT = 50
FIELD_FILTER = "level:info"

REQUEST_TEMPLATE = '{{"query": "{filter}", "sort": "@timestamp:desc", "size": {size}}}'


def fetch_recent_logs(field_filter="", size=MAX_RECENT):
    """Retrieve recent log results filtered by field values and time range.

    Returns a list of normalized log objects.
    """
    payload = {"query": field_filter or "", "sort": "@timestamp:desc", "size": size}
    url = get_log_service_url()
    headers = {**get_auth_header(), "Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        raw = response.json()
        logs = parse_log_response(raw)
        return logs
    except requests.RequestException as e:
        print(f"Error fetching logs: {e}")
        return []


if __name__ == "__main__":
    recent = fetch_recent_logs(field_filter=FIELD_FILTER)
    print(f"Recent logs ({len(recent)}):", recent)
