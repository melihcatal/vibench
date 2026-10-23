from security_client import kms_client

def embed_audit_notes(encrypted_data, audit_notes):
    return f'{encrypted_data}#audit#{audit_notes}'