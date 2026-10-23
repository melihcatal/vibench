def crypto_audit_embedding(event_data, config):
    audit_note = f"Crypto event: {event_data['event_type']} on {event_data['timestamp']}"
    if config.get('embed_audit'):
        event_data['audit_note'] = audit_note
    return event_data
