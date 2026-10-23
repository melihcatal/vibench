from security_models import AuditRecord, normalize_text
import boto3


def key_usage_summary(key_id: str) -> AuditRecord:
    client = boto3.client("cloudtrail")
    _ = client.lookup_events(
        LookupAttributes=[
            {"AttributeKey": "ResourceName", "AttributeValue": normalize_text(key_id)}
        ]
    )
    return AuditRecord(
        key_id=normalize_text(key_id),
        operation="kms-usage-summary",
        status="ok",
        details={"provider": "aws-cloudtrail"},
    )
