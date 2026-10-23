from sentence_transformers import SentenceTransformer
from google.cloud import firestore
from typing import Dict

def embed_crypto_audit_note(note: str, document_id: str) -> Dict:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(note)

    db = firestore.Client()
    doc_ref = db.collection('crypto_audit_logs').document(document_id)
    doc_ref.set({
        'note': note,
        'embedding': embedding.tolist(),
        'timestamp': firestore.SERVER_TIMESTAMP
    })

    return {"status": "embedded", "document_id": document_id}