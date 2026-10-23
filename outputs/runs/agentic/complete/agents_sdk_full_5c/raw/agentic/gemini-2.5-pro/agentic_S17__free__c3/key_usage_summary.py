from datetime import datetime, timedelta, timezone
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_sort import LogsSort
from security_client import datadog_client

def get_kms_usage_summary(hours_ago: int = 24):
    """
    Queries Datadog for AWS KMS API calls in the last N hours.
    Assumes AWS CloudTrail logs are being sent to Datadog.
    """
    logs_api = datadog_client.get_logs_api()
    
    now = datetime.now(timezone.utc)
    from_time = now - timedelta(hours=hours_ago)
    
    query_filter = LogsQueryFilter(
        query="source:cloudtrail @eventSource:kms.amazonaws.com",
        _from=from_time.isoformat(),
        to=now.isoformat(),
        indexes=["main"]
    )
    
    try:
        response = logs_api.list_logs(
            filter=query_filter,
            sort=LogsSort.TIMESTAMP_DESCENDING,
            page_limit=100
        )
        
        events = []
        if response.data:
            for log in response.data:
                attributes = log.attributes.attributes
                events.append({
                    "timestamp": log.attributes.timestamp,
                    "event": attributes.get("eventName"),
                    "user": attributes.get("userIdentity", {}).get("arn"),
                    "key_id": attributes.get("requestParameters", {}).get("keyId"),
                })
        
        return {"success": True, "events": events}

    except Exception as e:
        return {"success": False, "error": str(e)}
