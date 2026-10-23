def embed_crypto_audit(event):
    audit_note = f"Crypto event: {event['action']} with key_id {event['key_id']} and algorithm {event['algorithm']}"
    return audit_note