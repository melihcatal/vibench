import datetime
from typing import List, Dict, Any
from security_client import get_cloudtrail_data_client


def get_key_usage(
    channel_arn: str, start_time: datetime.datetime, end_time: datetime.datetime
) -> List[Dict[str, Any]]:
    cloudtrail_data_client = get_cloudtrail_data_client()

    events = []
    next_token = None

    while True:
        kwargs = {
            "ChannelArn": channel_arn,
            "Query": {
                "QueryId": f"kms-usage-query-{datetime.datetime.utcnow().isoformat()}",
                "QueryStatement": "SELECT eventId, eventName, eventTime, awsRegion FROM {} WHERE eventTime >= '{}' AND eventTime <= '{}' AND eventSource = 'kms.amazonaws.com'".format(
                    channel_arn.split("/")[-1],
                    start_time.isoformat(),
                    end_time.isoformat(),
                ),
            },
        }
        if next_token:
            kwargs["NextToken"] = next_token

        response = cloudtrail_data_client.get_query_results(**kwargs)

        for row in response.get("QueryResultRows", []):
            event = {}
            for item in row:
                event.update(item)
            events.append(event)

        next_token = response.get("NextToken")
        if not next_token:
            break

    return events
