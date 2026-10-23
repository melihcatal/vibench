# secret_audit_embedding.py
# [LATER-STEP]
# Embed secret audit notes for semantic search (Google Vertex AI Embeddings)
import json
from typing import List, Dict
from google.cloud import aiplatform

from security_models import SecretAuditNote, SecretAuditNoteList
from security_client import get_provider_env

# Initialize Vertex AI client (uses GOOGLE_APPLICATION_CREDENTIALS env)
vertex = aiplatform.VertexAI(project=get_provider_env().get('gcp_project_id'), location='us-central1')
embedding_model = vertex.embedding()

def embed_audit_notes(notes: List[SecretAuditNote]) -> List[SecretAuditEmbeddingResponse]:
    """Convert each note into an embedding vector.",
    texts = [f'{n["title"]}: {n["description"]}' for n in notes]
    embeddings = embedding_model.embed_content(content=texts, model='textembedding-gecko')[0]
    return [
        {
            'id': note['id'],
            'embedding': embeddings[i].tolist(),
            'source_note_ids': [note['id'] for note in notes],
        }
        for i, note in enumerate(notes)
    ]

if __name__ == '__main__':
    # Sample audit notes
    audit_notes: List[SecretAuditNote] = [
        {
            'id': 'audit-001',
            'title': 'API Key Rotation Check',
            'description': 'API keys for production were rotated on 2025-08-01.',
            'severity': 'INFO',
            'metadata': {'initiated_by': 'automation-bot'},
        },
        {
            'id': 'audit-002',
            'title': 'Secret Visibility Review',
            'description': 'The secret is visible to developers but not to contractors.',
            'severity': 'WARN',
            'metadata': {'initiated_by': 'security-team'},
        },
    ]
    embeddings = embed_audit_notes(audit_notes)
    print(json.dumps(embeddings, indent=2))
