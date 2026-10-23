from collections import Counter
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_sort import LogsSort

from security_client import get_datadog_logs_api

def get_key_usage_summary(query: str, time_range="now-1h", limit=100):
    """
    Summarizes crypto key usage by querying logs from Datadog.
    This function looks for logs matching a specific query (e.g., service:kms)
    and counts the occurrences of different event names or key IDs.
    """
    api = get_datadog_logs_api()

    # Example Datadog log query: "source:cloudtrail @evt.name:Encrypt OR @evt.name:Decrypt"
    filter_query = LogsQueryFilter(
        query=query,
        indexes=["main"],
        _from=time_range,
        to="now"
    )

    body = LogsListRequest(
        filter=filter_query,
        page=dict(
            limit=limit,
        ),
        sort=LogsSort.TIMESTAMP_DESCENDING,
    )

    try:
        response = api.list_logs(body=body)
    except Exception as e:
        return {"error": str(e)}

    event_summary = Counter()
    key_id_summary = Counter()

    if not response.data:
        return {"message": "No matching logs found."}

    for log in response.data:
        attributes = log.attributes.attributes
        # This is a sample structure; actual log attributes will vary.
        event_name = attributes.get("evt", {}).get("name")
        if event_name:
            event_summary[event_name] += 1

        # Attempt to find a key ID in a common location for AWS CloudTrail logs
        try:
            key_id = attributes.get("requestParameters", {}).get("keyId")
            if key_id:
                key_id_summary[key_id] += 1
        except (AttributeError, TypeError):
            continue

    return {
        "event_summary": dict(event_summary),
        "key_id_summary": dict(key_id_summary),
        "logs_found": len(response.data)
    }
