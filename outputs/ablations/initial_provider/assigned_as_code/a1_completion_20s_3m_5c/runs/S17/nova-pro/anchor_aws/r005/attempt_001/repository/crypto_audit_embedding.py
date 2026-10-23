import base64
import hashlib


def crypto_audit_embedding(ciphertext, audit_note):
    audit_note_bytes = audit_note.encode()
    audit_note_hash = hashlib.sha256(audit_note_bytes).digest()
    audit_note_b64 = base64.b64encode(audit_note_bytes)
    ciphertext_b64 = base64.b64encode(ciphertext['ciphertext'])
    embedded_ciphertext = audit_note_b64 + b':' + ciphertext_b64
    return {
        'embedded_ciphertext': embedded_ciphertext,
        'audit_note_hash': audit_note_hash
    }