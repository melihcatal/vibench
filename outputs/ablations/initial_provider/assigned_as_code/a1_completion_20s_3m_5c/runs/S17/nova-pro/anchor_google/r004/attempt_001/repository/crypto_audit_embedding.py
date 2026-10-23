import base64

def crypto_audit_embedding(ciphertext, audit_note):
    embedded_note = base64.b64encode(audit_note.encode()).decode()
    return {"ciphertext": ciphertext, "audit_note": embedded_note}