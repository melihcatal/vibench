import boto3
import datetime
from botocore.exceptions import ClientError

def summarize_key_usage(region: str, days_back: int = 7):
    kms_client = boto3.client("kms", region_name=region)
    cloudtrail_client = boto3.client("cloudtrail", region_name=region)

    summary = {
        "key_count": 0,
        "alias_count": 0,
        "crypto_events": []
    }

    try:
        # List keys
        keys = []
        paginator = kms_client.get_paginator("list_keys")
        for page in paginator.paginate():
            keys.extend(page["Keys"])
        summary["key_count"] = len(keys)

        # List aliases
        aliases = []
        paginator = kms_client.get_paginator("list_aliases")
        for page in paginator.paginate():
            aliases.extend(page["Aliases"])
        summary["alias_count"] = len(aliases)

        # Get crypto events from CloudTrail
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=days_back)

        # Search for KMS-related events in CloudTrail
        # Common KMS API actions include Encrypt, Decrypt, GenerateDataKey, Sign, Verify
        response = cloudtrail_client.lookup_events(
            LookupAttributes=[
                {
                    'AttributeKey': 'EventSource',
                    'AttributeValue': 'kms.amazonaws.com'
                },
            ],
            StartTime=start_time,
            EndTime=end_time
        )

        for event in response.get("Events", []):
            summary["crypto_events"].append({
                "event_name": event.get("EventName"),
                "event_time": event.get("EventTime").isoformat(),
                "username": event.get("Username"),
                "resource_type": event.get("Resources", [{}])[0].get("ResourceType"),
                "resource_name": event.get("Resources", [{}])[0].get("ResourceName"),
            })

    except ClientError as e:
        summary["error"] = str(e)

    return summary
