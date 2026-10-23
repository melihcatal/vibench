from typing import List
from identity_models import LoginAuditRecord
from datetime import datetime
import boto3
from botocore.config import Config


def summarize_audit_events(records: List[LoginAuditRecord]) -> dict:
    summary = {
        "total_logins": len(records),
        "providers": {},
        "status_distribution": {},
        "time_range": {
            "start": None,
            "end": None,
        },
    }
    
    for record in records:
        # Provider distribution
        if record.provider not in summary["providers"]:
            summary["providers"][record.provider] = 0
        summary["providers"][record.provider] += 1
        
        # Status distribution
        if record.status not in summary["status_distribution"]:
            summary["status_distribution"][record.status] = 0
        summary["status_distribution"][record.status] += 1
        
        # Time range
        timestamp = datetime.fromisoformat(record.timestamp)
        if summary["time_range"]["start"] is None or timestamp < summary["time_range"]["start"]:
            summary["time_range"]["start"] = timestamp
        if summary["time_range"]["end"] is None or timestamp > summary["time_range"]["end"]:
            summary["time_range"]["end"] = timestamp
    
    # Store summary in AWS CloudWatch
    cloudwatch = boto3.client(
        "cloudwatch",
        region_name="us-east-1",
        config=Config(retries={"max_attempts": 3}),
    )
    
    cloudwatch.put_metric_data(
        Namespace="FederatedLogin/Audit",
        MetricData=[
            {
                "MetricName": "TotalLogins",
                "Value": summary["total_logins"],
                "Unit": "Count",
            },
            {
                "MetricName": "SuccessfulLogins",
                "Value": summary["status_distribution"].get("success", 0),
                "Unit": "Count",
            },
        ],
    )
    
    return summary