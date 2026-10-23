from typing import Dict, List, Optional
import os
from datetime import datetime
from dataclasses import dataclass
import boto3
from botocore.exceptions import ClientError

@dataclass
class KeyUsageEvent:
    key_id: str
    event_type: str  # encrypt, decrypt, sign, verify
    timestamp: str
    status: str  # success, failed
    additional_info: Optional[Dict[str, str]] = None

class KeyUsageSummary:
    """Summarizes key usage events using AWS CloudTrail."""
    
    def __init__(self):
        self.cloudtrail = boto3.client(
            "cloudtrail",
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
    
    def log_event(self, event: KeyUsageEvent) -> None:
        """Logs a key usage event to AWS CloudTrail."""
        try:
            self.cloudtrail.put_event(
                TrailName=os.getenv("AWS_CLOUDTRAIL_NAME", "default"),
                EventData=event.__dict__
            )
        except ClientError as e:
            print(f"Failed to log event: {e}")
    
    def summarize_key_usage(self, key_id: str, start_time: datetime, end_time: datetime) -> List[Dict[str, str]]:
        """Summarizes key usage events for a given key and time range."""
        try:
            response = self.cloudtrail.lookup_events(
                LookupAttributes=[
                    {
                        "AttributeKey": "ResourceName",
                        "AttributeValue": key_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time
            )
            return [event["CloudTrailEvent"] for event in response["Events"]]
        except ClientError as e:
            print(f"Failed to summarize key usage: {e")
            return []