import os
import json
from typing import List, Dict, Any
from datetime import datetime
from security_models import KeyUsageEvent
import boto3
from botocore.exceptions import ClientError


class KeyUsageSummary:
    def __init__(self):
        self.cloudtrail = boto3.client(
            "cloudtrail",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def summarize_key_usage(
        self, key_id: str, lookback_hours: int = 24
    ) -> List[KeyUsageEvent]:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=lookback_hours)

        try:
            response = self.cloudtrail.lookup_events(
                LookupAttributes=[
                    {"AttributeKey": "ResourceName", "AttributeValue": key_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                MaxResults=50,
            )

            events = []
            for event in response.get("Events", []):
                events.append(
                    KeyUsageEvent(
                        key_id=key_id,
                        operation=event.get("EventName", "Unknown"),
                        status="Success"
                        if event.get("ErrorCode") is None
                        else "Failed",
                        timestamp=event.get("EventTime").isoformat(),
                        metadata={
                            "event_id": event.get("EventId"),
                            "username": event.get("Username"),
                        },
                    )
                )

            return events
        except ClientError as e:
            raise Exception(f"AWS CloudTrail lookup failed: {e}")
