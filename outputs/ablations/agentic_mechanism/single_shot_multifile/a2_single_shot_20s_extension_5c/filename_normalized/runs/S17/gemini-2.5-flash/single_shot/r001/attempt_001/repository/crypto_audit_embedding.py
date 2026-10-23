from security_client import SecurityClients
from typing import List

class AuditNoteEmbedding:
    def __init__(self, note_id: str, text: str, embedding: List[float]):
        self.note_id = note_id
        self.text = text
        self.embedding = embedding

def embed_audit_notes_cohere(notes_with_ids: List[Dict[str, str]], model: str = "embed-english-v3.0") -> List[AuditNoteEmbedding]:
    cohere_client = SecurityClients.get_cohere_client()

    texts = [note['text'] for note in notes_with_ids]
    note_ids = [note['id'] for note in notes_with_ids]
    
    response = cohere_client.embed(
        texts=texts,
        model=model,
        input_type="classification" # Using 'classification' input type as a common choice for audit notes.
    )
    
    embeddings = response.embeddings
    
    audit_embeddings = []
    for i, embedding in enumerate(embeddings):
        audit_embeddings.append(AuditNoteEmbedding(
            note_id=note_ids[i],
            text=texts[i],
            embedding=embedding
        ))
        
    return audit_embeddings