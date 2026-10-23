from summarize_secret_rotation import summarize_secret_rotation

def embed_secret_audit_notes(secret_name):
    summary = summarize_secret_rotation(secret_name)
    notes = ' '.join(summary['versions'].keys())
    return notes