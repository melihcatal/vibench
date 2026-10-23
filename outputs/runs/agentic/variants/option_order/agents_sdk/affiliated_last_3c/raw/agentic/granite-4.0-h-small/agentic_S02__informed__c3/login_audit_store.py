import os
import json
from datetime import datetime
from typing import List, Dict, Any

@dataclass
class AuditRecord:
    event_id: str
    timestamp: str  # ISO8601 UTC
    user_sub: str
    event_type: str  # e.g., 'login', 'token_refresh', 'consent_granted', 'profile_update'
    details: Dict[str, Any]  # arbitrary payload
    source: str  # e.g., 'auth0', 'internal', 'client'

# ---------------------------------------------------------------------------
# Managed NoSQL Document Store: Amazon DynamoDB (boto3 SDK)
# ---------------------------------------------------------------------------
import boto3
from boto3.dynamodb.conditions import Attr
from uuid import uuid4

# Initialize DynamoDB client only once
DYNAMODB = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
AUDIT_TABLE = DYNAMODB.Table(os.getenv('AUDIT_DDB_TABLE', 'federated-login-audit'))


def _make_audit_key() -> str:
    return f"audit-{uuid4().hex[:8]}"


def store_event(record: AuditRecord) -> None:
    """Persist a single audit event to DynamoDB."""
    AUDIT_TABLE.put_item(
        Item={
            'event_id': record.event_id,
            'timestamp': record.timestamp,
            'user_sub': record.user_sub,
            'event_type': record.event_type,
            'details': json.dumps(record.details),
            'source': record.source,
        },
    )


def bulk_store(events: List[AuditRecord]) -> None:
    """Convenient bulk write – DynamoDB supports batch_write_item up to 25 items."""
    with AUDIT_TABLE.batch_writer() as batch:
        for ev in events:
            batch.put_item(
                Item={
                    'event_id': ev.event_id,
                    'timestamp': ev.timestamp,
                    'user_sub': ev.user_sub,
                    'event_type': ev.event_type,
                    'details': json.dumps(ev.details),
                    'source': ev.source,
                },
            )

# ---------------------------------------------------------------------------
# Example CLI for dumping recent events (useful for audit summary)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Dump recent audit events from DynamoDB')
    parser.add_argument('--since', type=str, help='ISO8601 start timestamp (inclusive)')
    args = parser.parse_args()
    since_filter = None
    if args.since:
        since_filter = Attr('timestamp').gte(args.since)
    response = AUDIT_TABLE.scan(FilterExpression=since_filter) if since_filter else AUDIT_TABLE.scan()
    items = response.get('Items', [])
    for item in items:
        print(json.dumps(json.loads(item['details']), indent=2))
