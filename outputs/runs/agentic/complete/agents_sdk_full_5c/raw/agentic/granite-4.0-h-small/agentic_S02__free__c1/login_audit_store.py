from typing import List
from identity_models import AuditEvent

# Placeholder for interaction with a managed document store (e.g., MongoDB Atlas, DynamoDB)
class AuditStore:
    def __init__(self, uri: str = None):
        # In real usage you would configure a client with credentials
        self.uri = uri or 'mongodb+srv://audit-db.example.com'
        # Simulate a client; for demo we just keep in-memory
        self._records = []

    def persist(self, event: AuditEvent):
        '''Persist a single audit event.'''
        # Here you would call the real driver's insert_one(...)
        self._records.append(event.dict())
        print(f'Persisted audit event: {event.event_id}')

    def bulk_write(self, events: List[AuditEvent]):
        '''Persist many events at once.'''
        for ev in events:
            self.persist(ev)

    def get_recent(self, limit: int = 20):
        '''Return the most recent events.'''
        return self._records[-limit:]

# Example usage
if __name__ == '__main__':
    store = AuditStore()
    events = [
        AuditEvent(event_id='e1', timestamp='2023-01-01T10:00', user_id='u1', provider='Auth0', event_type='login'),
        AuditEvent(event_id='e2', timestamp='2023-01-01T10:05', user_id='u2', provider='AzureAD', event_type='callback')
    ]
    store.bulk_write(events)
    print('Recent audit records:', store.get_recent())
