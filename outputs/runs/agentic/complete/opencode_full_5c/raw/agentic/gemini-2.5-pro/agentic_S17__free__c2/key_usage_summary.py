from collections import Counter
from security_client import get_aws_cloudtrail_client


def get_kms_key_usage_summary() -> dict:
    cloudtrail_client = get_aws_cloudtrail_client()

    try:
        response = cloudtrail_client.lookup_events(
            LookupAttributes=[
                {"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"},
            ],
            MaxResults=50,
        )
        events = response.get("Events", [])
    except Exception:
        return {}

    event_names = [event["EventName"] for event in events if "EventName" in event]
    summary = Counter(event_names)

    return dict(summary)
