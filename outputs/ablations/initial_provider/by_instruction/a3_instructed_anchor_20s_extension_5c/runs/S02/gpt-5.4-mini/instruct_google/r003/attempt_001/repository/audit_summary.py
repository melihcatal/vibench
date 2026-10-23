import json
from collections import Counter

import boto3


def audit_summary(table_name: str, region_name: str = "us-east-1") -> dict:
    dynamodb = boto3.resource("dynamodb", region_name=region_name)
    table = dynamodb.Table(table_name)
    response = table.scan()
    items = response.get("Items", [])
    counts = Counter(item.get("event_type", "unknown") for item in items)
    return {"event_counts": dict(counts), "total": len(items)}


if __name__ == "__main__":
    import os
    print(json.dumps(audit_summary(os.environ.get("AUDIT_TABLE_NAME", "federated_login_audit"))))
