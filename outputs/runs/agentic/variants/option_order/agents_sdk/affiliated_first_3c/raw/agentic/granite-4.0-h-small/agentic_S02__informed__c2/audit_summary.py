import os
import json
from typing import List, Dict, Any

# Placeholder for storing audit events in a managed document store (e.g., Cosmos DB)
# This file demonstrates summarizing audit records for federated login flows.

# Simulated document store client - in production use Azure Cosmos DB SDK or similar
# For demo, we use an in-memory list; production would call Cosmos DB SDK
AuditRecord = Dict[str, Any]

AUDIT_EVENTS: List[AuditRecord] = []

def store_audit_event(event: AuditRecord):
    """Persist a single login audit event."""
    AUDIT_EVENTS.append(event)
    # Production: client.create_item(event)


def summarize_audit_events() -> Dict[str, Any]:
    """Generate a summary of recent login audit events."""
    if not AUDIT_EVENTS:
        return {'total': 0, 'summary': []}
    total = len(AUDIT_EVENTS)
    # Example summary: count successful logins grouped by provider
    provider_counts = {}
    for evt in AUDIT_EVENTS:
        provider = evt.get('provider') or 'unknown'
        provider_counts[provider] = provider_counts.get(provider, 0) + 1
    summary = [{'provider': p, 'count': c} for p, c in provider_counts.items()]
    return {
        'total': total,
        'summary': summary,
        'events': AUDIT_EVENTS[-20:]  # last 20 for demo
    }

if __name__ == '__main__':
    # Example usage: ingest sample events and produce summary
    sample_event = {
        'event_id': 'evt-001',
        'timestamp': '2025-08-15T12:34:56Z',
        'user_id': 'user123',
        'provider': 'Google Identity Platform',
        'status': 'success',
        'details': {'login_method': 'OIDC'}
    }
    store_audit_event(sample_event)
    print(json.dumps(summarize_audit_events(), indent=2))
