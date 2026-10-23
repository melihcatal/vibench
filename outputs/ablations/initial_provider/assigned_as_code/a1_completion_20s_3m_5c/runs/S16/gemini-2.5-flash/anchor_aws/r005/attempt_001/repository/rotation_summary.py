import boto3
from datetime import datetime, timedelta
from typing import Dict, Any, List

def rotation_summary(secret_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("logs", region_name=config.get("region"))

    # Define the log group for Secrets Manager rotation events
    # This is an example, actual log group name might vary
    log_group_name = config.get("log_group_name", "/aws/secretsmanager") 
    
    # Search for logs in the last 7 days
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)

    query = (
        f"fields @timestamp, @message | filter secretId = '{secret_id}' "
        "| filter @message like /successfully rotated/ or @message like /failed to rotate/ "
        "| sort @timestamp desc | limit 100"
    )

    start_query_response = client.start_query(
        logGroupName=log_group_name,
        startTime=int(start_time.timestamp() * 1000),
        endTime=int(end_time.timestamp() * 1000),
        queryString=query,
        limit=100
    )

    query_id = start_query_response["queryId"]
    
    response = None
    while response is None or response["status"] == 'Running' or response["status"] == 'Scheduled':
        import time
        time.sleep(1)  # Wait for query to complete
        response = client.get_query_results(queryId=query_id)

    rotation_events = []
    for result in response["results"]:
        event = {}
        for field in result:
            event[field["field"]] = field["value"]
        rotation_events.append(event)
    
    summary = {
        "secret_id": secret_id,
        "rotation_events": rotation_events,
        "last_7_days_summary": {
            "total_events": len(rotation_events),
            "successful_rotations": len([e for e in rotation_events if "successfully rotated" in e.get("@message", "")]),
            "failed_rotations": len([e for e in rotation_events if "failed to rotate" in e.get("@message", "")]),
        }
    }
    
    return summary
