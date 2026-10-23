import os
import json
import uuid
from datetime import datetime, timezone
import boto3
from identity_models import ProfileClaims

# Managed NoSQL Document Store (AWS DynamoDB) configuration for audit records
DYNAMODB_TABLE = os.getenv('AUDIT_TABLE_NAME')
if not DYNAMODB_TABLE:
    raise RuntimeError('AUDIT_TABLE_NAME environment variable not set')

ddb = boto3.resource('dynamodb')
audit_table = ddb.Table(DYNAMODB_TABLE)

AUDIT_PARTITION_KEY = 'eventId'

@dataclass

class AuditRecord:
    '''Immutable audit event persisted after login.'''
    event_id: str
    user_id: str
    profile: ProfileClaims
    auth_method: str  # e.g., 'oauth', 'pkce', 'federated'
    auth_provider: str  # e.g., 'azure', 'cognito'
    timestamp: int  # epoch seconds
    details: Dict[str, Any]

    @classmethod
    def from_request(cls, auth_method: str, auth_provider: str, tokens: Dict[str, Any], profile: ProfileClaims, extra: Dict[str, Any] = None) -> 'AuditRecord':
        extra = extra or {}
        return cls(
            event_id=str(uuid.uuid4()),
            user_id=profile.user_id,
            profile=profile,
            auth_method=auth_method,
            auth_provider=auth_provider,
            timestamp=int(datetime.now(timezone.utc).timestamp()),
            details={**tokens, **extra}
        )

    def to_dynamodb_item(self) -> Dict[str, Any]:
        return {
            AUDIT_PARTITION_KEY: self.event_id,
            'timestamp': self.timestamp,
            'user_id': self.user_id,
            'profile': json.dumps(asdict(self.profile)),
            'auth_method': self.auth_method,
            'auth_provider': self.auth_provider,
            'details': self.details
        }

    @staticmethod
    def retrieve_latest(limit: int = 20) -> List[Dict[str, Any]]:
        '''Fetch the most recent audit entries.'''
        response = audit_table.query(
            IndexName='timestamp-index',  # Ensure a GSI on timestamp descending
            KeyConditionExpression=boto3.dynamodb.conditions.Key(AUDIT_PARTITION_KEY).begins_with(''),
            ScanIndexForward=False,
            Limit=limit
        )
        items = response.get('Items', [])
        # Convert stored JSON strings back to ProfileClaims objects for convenience
        parsed = []
        for it in items:
            it['profile'] = ProfileClaims(**json.loads(it['profile']))
            parsed.append(it)
        return parsed


def persist_audit_event(audit: AuditRecord):
    '''Write an audit record to DynamoDB.'''
    item = audit.to_dynamodb_item()
    audit_table.put_item(Item=item)

if __name__ == '__main__':
    # Simple CLI demo: create a mock audit entry & fetch latest
    demo_profile = ProfileClaims(
        user_id='demo-001',
        email='demo@example.com',
        email_verified=True,
        given_name='Demo',
        family_name='User',
        picture_url='https://example.com/avatar.png'
    )
    demo_audit = AuditRecord.from_request(
        auth_method='oauth',
        auth_provider='azure',
        tokens={'access_token': 'mock-123', 'id_token': 'mock-id'},
        profile=demo_profile,
        extra={'scope': 'openid profile email'}
    )
    persist_audit_event(demo_audit)
    latest = AuditRecord.retrieve_latest(limit=5)
    print(json.dumps(latest, indent=2))
