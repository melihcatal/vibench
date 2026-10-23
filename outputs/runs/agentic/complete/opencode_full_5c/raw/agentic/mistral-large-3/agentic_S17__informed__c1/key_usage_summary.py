import os
from typing import List, Dict, Any
import boto3
from datetime import datetime
from security_models import KeyUsageEvent


class KeyUsageSummarizer:
    def __init__(self):
        self.cloudtrail_client = boto3.client(
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
            response = self.cloudtrail_client.lookup_events(
                LookupAttributes=[
                    {"AttributeKey": "ResourceName", "AttributeValue": key_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                MaxResults=50,
            )

            events = []
            for event in response["Events"]:
                events.append(
                    KeyUsageEvent(
                        key_id=key_id,
                        event_type=event["EventName"],
                        timestamp=event["EventTime"].isoformat(),
                        metadata={
                            "event_id": event["EventId"],
                            "username": event.get("Username", "unknown"),
                            "resources": event.get("Resources", []),
                        },
                    )
                )
            return events
        except Exception as e:
            raise Exception(f"Failed to summarize key usage: {e}")
